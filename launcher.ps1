$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$profileDir = "C:\playwright_edge_profile"

Stop-Process -Name "msedge" -ErrorAction SilentlyContinue

Write-Host "Starting Edge..." -ForegroundColor Cyan
Start-Process $edgePath -ArgumentList "--remote-debugging-port=9222", "--user-data-dir=$profileDir", "--no-first-run"

Write-Host "Waiting 10 seconds for port 9222..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "Starting solve.py..." -ForegroundColor Yellow
python solve.py

Write-Host "Done." -ForegroundColor Green