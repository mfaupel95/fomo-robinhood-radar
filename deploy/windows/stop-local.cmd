@echo off
REM Stop the local FOMO Radar stack.
setlocal
echo [stop] api / site
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r /c:":8000 .*LISTENING" /c:":4321 .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [stop] bot
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match 'fomo_agent.cli bot' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1
echo done.
endlocal
