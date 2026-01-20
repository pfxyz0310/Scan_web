@echo off
echo 正在開啟可被 Python 控制的 Chrome...
echo 請在這個 Chrome 視窗中登入 HyRead 並打開電子書
echo.

:: 設定使用者資料夾 (這樣可以保留你的登入資訊，不用每次重登)
set USER_DIR=%~dp0\chrome_profile

:: 啟動 Chrome 並開啟遠端除錯埠 9222
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USER_DIR%"

pause