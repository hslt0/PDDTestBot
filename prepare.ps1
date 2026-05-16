$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$profileDir = "C:\playwright_edge_profile"

Write-Host "Starting Edge..." -ForegroundColor Cyan

Stop-Process -Name "msedge" -ErrorAction SilentlyContinue

Start-Process $edgePath -ArgumentList "--remote-debugging-port=9222", "--user-data-dir=$profileDir", "--no-first-run"

Read-Host -Prompt "Enter any key to stop"