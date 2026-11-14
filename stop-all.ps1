<#
.SYNOPSIS
    Stops the Aegis services started by start-all.ps1.

.DESCRIPTION
    Stops only python / node processes that are listening on the Aegis
    ports (8000 backend, 8765 camera agent, 5173 frontend). Other programs
    are never touched.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\stop-all.ps1
#>
$ports = @{ 8000 = 'backend'; 8765 = 'camera agent'; 5173 = 'frontend' }

foreach ($port in $ports.Keys) {
    $listeners = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($null -eq $listeners) {
        Write-Host ("{0} (port {1}): not running" -f $ports[$port], $port)
        continue
    }
    foreach ($procId in ($listeners | Select-Object -ExpandProperty OwningProcess -Unique)) {
        $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if ($null -eq $proc) { continue }
        if ($proc.ProcessName -notin @('python', 'pythonw', 'node')) {
            Write-Host ("{0} (port {1}): used by '{2}', left running" -f $ports[$port], $port, $proc.ProcessName) -ForegroundColor Yellow
            continue
        }
        Stop-Process -Id $procId -Force
        Write-Host ("{0} (port {1}): stopped {2} (pid {3})" -f $ports[$port], $port, $proc.ProcessName, $procId) -ForegroundColor Green
    }
}

# Close the windows start-all.ps1 opened (identified by their exact titles).
$titles = @('Aegis backend', 'Aegis camera agent', 'Aegis frontend')
Get-Process powershell -ErrorAction SilentlyContinue |
    Where-Object { $titles -contains $_.MainWindowTitle } |
    ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host ("closed window '{0}'" -f $_.MainWindowTitle)
    }
