@echo off
echo ========================================
echo Building YouTube Downloader Executable
echo ========================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Clean previous build
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

echo Cleaning completed...
echo.

REM Build executable
echo Building executable with PyInstaller...
echo.
pyinstaller --onefile --noconsole --name="YouTube_Downloader" YouToMp3.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: dist\YouTube_Downloader.exe
    echo File size: 
    dir dist\YouTube_Downloader.exe | findstr YouTube_Downloader.exe
    echo.
    echo You can now run: dist\YouTube_Downloader.exe
    echo.
) else (
    echo.
    echo ========================================
    echo Build failed! Please check errors above.
    echo ========================================
)

pause
