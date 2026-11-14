<#
.SYNOPSIS
    Starts Aegis on Windows: backend API (8000), camera agent (8765) and
    frontend (5173), each in its own PowerShell window.

.DESCRIPTION
    Checks prerequisites first and stops with a clear message if something
    is missing. It never changes the database: if migrations are pending it
    tells you the command to run instead of running it.

.PARAMETER CheckOnly
    Only run the prerequisite checks.

.PARAMETER NoAgent
    Do not start the camera agent (lessons will wait for it).

.PARAMETER NoBrowser
    Do not open http://localhost:5173 at the end.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\start-all.ps1
    powershell -ExecutionPolicy Bypass -File .\start-all.ps1 -CheckOnly
#>
param(
    [switch]$CheckOnly,
    [switch]$NoAgent,
    [switch]$NoBrowser,
    [ValidateSet('Normal', 'Minimized')]
    [string]$WindowStyle = 'Normal'
)

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$Backend = Join-Path $Root 'backend'
$Frontend = Join-Path $Root 'frontend'
$Facial = Join-Path $Root 'facial_analysis'
$AgentPython = Join-Path $Facial 'venv\Scripts\python.exe'
$problems = New-Object System.Collections.Generic.List[string]

function Write-Check([string]$Name, [bool]$Ok, [string]$Hint) {
    if ($Ok) {
        Write-Host ("  [ OK ] " + $Name) -ForegroundColor Green
    } else {
        Write-Host ("  [FAIL] " + $Name) -ForegroundColor Red
        if ($Hint) { Write-Host ("         " + $Hint) -ForegroundColor Yellow }
        $problems.Add($Name)
    }
}

function Test-PortFree([int]$Port) {
    $listening = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return ($null -eq $listening)
}

function Wait-Http([string]$Url, [int]$Seconds) {
    $deadline = (Get-Date).AddSeconds($Seconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $null = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            return $true
        } catch {
            Start-Sleep -Milliseconds 700
        }
    }
    return $false
}

Write-Host ''
Write-Host 'Aegis - checking prerequisites' -ForegroundColor Cyan

$python = Get-Command python -ErrorAction SilentlyContinue
Write-Check 'Python on PATH (backend)' ($null -ne $python) 'Install Python 3.10+ and tick "Add python.exe to PATH".'
$npm = Get-Command npm -ErrorAction SilentlyContinue
Write-Check 'Node.js / npm on PATH (frontend)' ($null -ne $npm) 'Install Node.js 20 LTS or newer.'
Write-Check 'backend\.env exists' (Test-Path (Join-Path $Backend '.env')) 'Copy backend\.env.example to backend\.env and fill in DATABASE_URL and SECRET_KEY.'
Write-Check 'frontend\node_modules installed' (Test-Path (Join-Path $Frontend 'node_modules')) 'Run: cd frontend; npm install'
if (-not $NoAgent) {
    Write-Check 'facial_analysis\venv exists (camera agent)' (Test-Path $AgentPython) 'Run: cd facial_analysis; python -m venv venv; .\venv\Scripts\pip install -r requirements.txt'
}

foreach ($p in @(@{Port = 8000; Name = 'backend'}, @{Port = 5173; Name = 'frontend'}, @{Port = 8765; Name = 'camera agent'})) {
    if ($NoAgent -and $p.Port -eq 8765) { continue }
    Write-Check ("Port {0} free ({1})" -f $p.Port, $p.Name) (Test-PortFree $p.Port) 'Something is already running there. Close it or run .\stop-all.ps1.'
}

if ($null -ne $python -and (Test-Path (Join-Path $Backend '.env'))) {
    # Reads the migration state; never changes the database.
    # alembic logs to stderr; Windows PowerShell 5.1 would treat that as a
    # terminating error under ErrorActionPreference=Stop.
    Push-Location $Backend
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $current = (& python -m alembic current 2>&1 | Out-String)
    } finally {
        $ErrorActionPreference = $previousPreference
        Pop-Location
    }
    $reachable = ($current -notmatch 'OperationalError|could not connect|password authentication failed|does not exist')
    Write-Check 'PostgreSQL reachable with backend\.env settings' $reachable 'Start PostgreSQL and check DATABASE_URL in backend\.env.'
    if ($reachable) {
        Write-Check 'Database schema up to date (alembic head)' ($current -match '\(head\)') 'Run: cd backend; python -m alembic upgrade head   (back up first, see README)'
    }
}

if ($problems.Count -gt 0) {
    Write-Host ''
    Write-Host ("{0} check(s) failed. Fix them and run this script again." -f $problems.Count) -ForegroundColor Red
    exit 1
}
Write-Host 'All checks passed.' -ForegroundColor Green
if ($CheckOnly) { exit 0 }

Write-Host ''
Write-Host 'Starting backend on http://127.0.0.1:8000 ...' -ForegroundColor Cyan
$backendCmd = "`$host.UI.RawUI.WindowTitle = 'Aegis backend'; `$env:PYTHONPATH = '$Backend'; Set-Location '$Root'; python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"
Start-Process powershell -ArgumentList @('-NoExit', '-Command', $backendCmd) -WindowStyle $WindowStyle
if (-not (Wait-Http 'http://127.0.0.1:8000/' 45)) {
    Write-Host 'The backend did not start within 45 s. Read the "Aegis backend" window for the error.' -ForegroundColor Red
    exit 1
}
Write-Host '  backend is up' -ForegroundColor Green

if (-not $NoAgent) {
    Write-Host 'Starting camera agent on http://127.0.0.1:8765 (webcam stays off until a lesson starts) ...' -ForegroundColor Cyan
    $agentCmd = "`$host.UI.RawUI.WindowTitle = 'Aegis camera agent'; Set-Location '$Facial'; & '$AgentPython' main.py"
    Start-Process powershell -ArgumentList @('-NoExit', '-Command', $agentCmd) -WindowStyle $WindowStyle
    if (Wait-Http 'http://127.0.0.1:8765/status' 30) {
        Write-Host '  camera agent is up' -ForegroundColor Green
    } else {
        Write-Host '  camera agent did not answer yet - check the "Aegis camera agent" window.' -ForegroundColor Yellow
    }
}

Write-Host 'Starting frontend on http://localhost:5173 ...' -ForegroundColor Cyan
$frontendCmd = "`$host.UI.RawUI.WindowTitle = 'Aegis frontend'; Set-Location '$Frontend'; npm run dev"
Start-Process powershell -ArgumentList @('-NoExit', '-Command', $frontendCmd) -WindowStyle $WindowStyle
if (-not (Wait-Http 'http://127.0.0.1:5173/' 45)) {
    Write-Host 'The frontend did not start within 45 s. Read the "Aegis frontend" window for the error.' -ForegroundColor Red
    exit 1
}
Write-Host '  frontend is up' -ForegroundColor Green

Write-Host ''
Write-Host 'Aegis is running: http://localhost:5173' -ForegroundColor Green
Write-Host 'Stop everything with: .\stop-all.ps1 (or close the three windows).'
if (-not $NoBrowser) { Start-Process 'http://localhost:5173' }
