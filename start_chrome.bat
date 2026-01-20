@echo off
echo 正在開啟可被 Python 控制的 Chrome...
echo 請在這個 Chrome 視窗中登入目標網站並打開欲掃描的內容
echo.

set USER_DIR=%~dp0\chrome_profile
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USER_DIR%"

pause