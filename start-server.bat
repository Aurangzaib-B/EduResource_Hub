@echo off
echo =========================================
echo    EduResource Hub - Local Server
echo =========================================
echo.
echo Starting local development server...
echo This will open your website in the browser.
echo.
echo Press Ctrl+C to stop the server when done.
echo.
pause

REM Try Python 3 first, then Python 2
python server.py 2>nul
if errorlevel 1 (
    python3 server.py 2>nul
    if errorlevel 1 (
        echo.
        echo ERROR: Python is not installed or not in PATH
        echo.
        echo Please install Python from https://python.org
        echo Or run the server manually with one of these commands:
        echo   python -m http.server 8000
        echo   python3 -m http.server 8000
        echo.
        pause
    )
)
