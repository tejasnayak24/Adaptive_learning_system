# Poll backend until it's available, then run smoke tests
$base = 'http://127.0.0.1:8000'

Function Wait-ForBackend {
    param($url, $timeoutSec=60)
    $start = Get-Date
    while ( ( (Get-Date) - $start ).TotalSeconds -lt $timeoutSec ) {
        try {
            $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2
            Write-Output "Backend available: $url (Status $($r.StatusCode))"
            return $true
        } catch {
            Write-Output "Waiting for backend..."
            Start-Sleep -Seconds 2
        }
    }
    return $false
}

if (-not (Wait-ForBackend "$base/" 60)) {
    Write-Error "Backend did not respond within timeout."
    exit 2
}

# Helper to POST JSON and return PS object
Function PostJson($path, $body, $token=$null) {
    $uri = "$base$path"
    $headers = @{}
    if ($token) { $headers['Authorization'] = "Bearer $token" }
    try {
        $resp = Invoke-RestMethod -Method Post -Uri $uri -Body (ConvertTo-Json $body -Depth 5) -ContentType 'application/json' -Headers $headers -TimeoutSec 30
        return @{ success=$true; data=$resp }
    } catch {
        return @{ success=$false; error=$_.Exception.Response.StatusCode.Value__ -as [string]; message=$_.Exception.Message }
    }
}

Function GetJson($path, $token=$null) {
    $uri = "$base$path"
    $headers = @{}
    if ($token) { $headers['Authorization'] = "Bearer $token" }
    try {
        $resp = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers -TimeoutSec 30
        return @{ success=$true; data=$resp }
    } catch {
        return @{ success=$false; message=$_.Exception.Message }
    }
}

# 1) Try register a new user
$ts = [int][double]::Parse((Get-Date -UFormat %s))
$email = "smoketest+$ts@example.com"
$pw = "TestPassword123!"
$name = "Smoke Tester"

Write-Output "Registering user $email ..."
$reg = PostJson "/auth/register" @{ name=$name; email=$email; password=$pw }
if (-not $reg.success) { Write-Output "Register failed: $($reg | ConvertTo-Json -Depth 3)" }
else { Write-Output "Register success: $($reg.data | ConvertTo-Json -Depth 3)" }

# 2) Login
Write-Output "Logging in..."
$login = PostJson "/auth/login" @{ email=$email; password=$pw }
if (-not $login.success) {
    Write-Output "Login JSON failed, trying /token form fallback..."
    try {
        $tokenResp = Invoke-RestMethod -Method Post -Uri "$base/token" -Body @{ username=$email; password=$pw } -ContentType 'application/x-www-form-urlencoded' -TimeoutSec 30
        $access = $tokenResp.access_token
        if ($access) { $token = $access; Write-Output "Token obtained via /token" }
    } catch {
        Write-Error "Login failed: $($login.message)"
        exit 3
    }
} else {
    # Try several common token locations in the JSON response
    $token = $null
    if ($login.data -is [System.Collections.Hashtable] -or $login.data -is [System.Object]) {
        if ($login.data.ContainsKey('access_token')) { $token = $login.data['access_token'] }
        elseif ($login.data.ContainsKey('token')) { $token = $login.data['token'] }
        elseif ($login.data.ContainsKey('data') -and $login.data['data'].ContainsKey('access_token')) { $token = $login.data['data']['access_token'] }
    }
    if (-not $token) {
        Write-Output "Login response, token not found. Inspecting response: $($login.data | ConvertTo-Json -Depth 3)"
        try {
            $tokenResp = Invoke-RestMethod -Method Post -Uri "$base/token" -Body @{ username=$email; password=$pw } -ContentType 'application/x-www-form-urlencoded' -TimeoutSec 30
            $token = $tokenResp.access_token
            if ($token) { Write-Output "Token obtained via /token fallback" }
        } catch {
            Write-Error "Could not obtain token; aborting smoke tests."
            exit 4
        }
    }
}

Write-Output "Token: $($token.Substring(0,20) + '...')"

# 3) Get lessons to pick one
 $less = GetJson "/lessons" $token
 if (-not $less.success) { Write-Output "Failed to fetch lessons: $($less.message)"; exit 5 }
 $lessons = $less.data
 if (-not ($lessons -is [System.Collections.IEnumerable])) {
     if ($lessons -and $lessons.ContainsKey('data')) { $lessons = $lessons['data'] }
     elseif ($lessons -and $lessons.ContainsKey('lessons')) { $lessons = $lessons['lessons'] }
     else { $lessons = @() }
 }
 if ($lessons.Count -eq 0) { Write-Output "No lessons available"; exit 6 }
 $lesson = $lessons[0]
 $lessonId = $null
 if ($lesson -and $lesson.ContainsKey('id')) { $lessonId = $lesson['id'] }
 elseif ($lesson -and $lesson.ContainsKey('lesson_id')) { $lessonId = $lesson['lesson_id'] }
 elseif ($lesson -and $lesson.ContainsKey('quiz_id')) { $lessonId = $lesson['quiz_id'] }
 if (-not $lessonId) { Write-Error "Could not determine lesson id"; exit 6 }
Write-Output "Selected lesson id: $lessonId"

# 4) Start quiz: try POST /quiz/start then GET /quiz/{id}
$start = PostJson "/quiz/start" @{ quiz_id = $lessonId } $token
if ($start.success) { $quizData = $start.data } else {
    Write-Output "Start quiz failed, trying GET /quiz/$lessonId"
    $getq = GetJson "/quiz/$lessonId" $token
    if (-not $getq.success) { Write-Error "Failed to load quiz"; exit 7 }
    $quizData = $getq.data
}
Write-Output "Quiz loaded: $($quizData | ConvertTo-Json -Depth 4)"

# 5) Submit quiz
$quiz_score = 80
$response_time = 12.5
$attention_score = 0.9
 $difficulty = "MEDIUM"
 if ($quizData -and $quizData.ContainsKey('quiz') -and $quizData['quiz'].ContainsKey('difficulty')) { $difficulty = $quizData['quiz']['difficulty'] }
 elseif ($quizData -and $quizData.ContainsKey('difficulty')) { $difficulty = $quizData['difficulty'] }

 # Determine student id from login response if present
 $student_id = $null
 if ($login.data -and $login.data.ContainsKey('user') -and $login.data['user'].ContainsKey('id')) { $student_id = $login.data['user']['id'] }
 elseif ($login.data -and $login.data.ContainsKey('id')) { $student_id = $login.data['id'] }
 if (-not $student_id) { $student_id = 0 }

 $payload = @{ student_id = $student_id; lesson_id = $lessonId; quiz_score = $quiz_score; response_time = $response_time; attention_score = $attention_score; difficulty = $difficulty }
Write-Output "Submitting quiz: $($payload | ConvertTo-Json)"
$submit = PostJson "/quiz/submit" $payload $token
if (-not $submit.success) { Write-Error "Quiz submit failed: $($submit | ConvertTo-Json -Depth 4)"; exit 8 }
Write-Output "Submit response: $($submit.data | ConvertTo-Json -Depth 4)"

# 6) Call RL recommend
 $subj = $lesson['subject'] -or $lesson['topic'] -or $lesson['title'] -or "General"
 $topic = $lesson['topic'] -or $lesson['title'] -or ""
 $ltitle = $lesson['title'] -or ""
 $rlReq = @{ subject = $subj; topic = $topic; lesson = $ltitle; previous_quiz_score = 60; current_quiz_score = $quiz_score; attention_score = $attention_score; yawning = $false; looking_away = $false; difficulty = $difficulty; response_time = $response_time; hints_used = 0; lesson_attempts = 1; completed_lessons = 1 }
Write-Output "Requesting RL recommendation..."
$rl = PostJson "/rl/recommend" $rlReq $token
if (-not $rl.success) { Write-Error "RL call failed: $($rl | ConvertTo-Json -Depth 4)"; exit 9 }
Write-Output "RL response: $($rl.data | ConvertTo-Json -Depth 4)"

# 7) Fetch progress
$studentId = $payload.student_id
$prog = GetJson "/progress/$studentId" $token
if (-not $prog.success) { Write-Error "Progress fetch failed: $($prog | ConvertTo-Json -Depth 3)"; exit 10 }
Write-Output "Progress: $($prog.data | ConvertTo-Json -Depth 4)"

Write-Output "Smoke tests completed successfully."