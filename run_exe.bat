@echo off
echo Starting YouTube Downloader...
echo.

REM Check if executable exists
if not exist "dist\YouTube_Downloader.exe" (
    echo ERROR: YouTube_Downloader.exe not found!
    echo Please run build_exe.bat first to create the executable.
    echo.
    pause
    exit /b 1
)

REM Run the executable
start "" "dist\YouTube_Downloader.exe"

echo YouTube Downloader started!
echo You can close this window now.
