@echo off
setlocal

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    echo Please install Python first or add it to PATH.
    pause
    exit /b 1
)

echo Starting local web server...
start "Parcel Precheck Server" cmd /k "cd /d ""%~dp0"" && python run_web.py"

timeout /t 2 >nul
start "" "http://127.0.0.1:5000"

exit /b 0
