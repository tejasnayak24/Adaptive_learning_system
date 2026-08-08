$urls = @(
  'http://127.0.0.1:8000',
  'http://127.0.0.1:8080',
  'http://127.0.0.1:5000',
  'http://127.0.0.1:8001',
  'http://localhost:8000',
  'http://localhost:8080',
  'http://localhost:5000'
)

foreach ($u in $urls) {
  try {
    $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 3
    Write-Output "$u => $($r.StatusCode)"
  }
  catch {
    Write-Output "$u => ERROR: $($_.Exception.Message)"
  }
}
