$o = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/openapi.json' -UseBasicParsing -TimeoutSec 10
if ($o -and $o.paths) {
  $o.paths.Keys | Sort-Object | ForEach-Object { Write-Output $_ }
} else {
  Write-Output 'No paths found'
}
