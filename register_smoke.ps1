$base='http://127.0.0.1:8000'
$body=@{name='smoketest'; email='smoketest+abc@example.com'; password='TestPassword123!'}
try {
  $r = Invoke-RestMethod -Method Post -Uri ($base + '/auth/register') -Body (ConvertTo-Json $body) -ContentType 'application/json' -TimeoutSec 30
  Write-Output "REGISTER OK:"
  $r | ConvertTo-Json -Depth 3 | Write-Output
} catch {
  Write-Output "REGISTER ERROR: $($_.Exception.Message)"
}
