# YouTube Downloader - MP3 & MP4 Launcher
# Ensures FFmpeg is accessible by refreshing environment variables

Write-Host "YouTube Downloader - MP3 & MP4" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""

# Change to script directory
Set-Location -Path $PSScriptRoot

# Refresh environment variables to ensure FFmpeg is accessible
Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Check if FFmpeg is accessible
Write-Host "Checking FFmpeg availability..." -ForegroundColor Yellow
try {
    $ffmpegVersion = & ffmpeg -version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ FFmpeg is available" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ FFmpeg not found in PATH. Audio conversion may fail." -ForegroundColor Red
    Write-Host "Make sure FFmpeg is installed and added to your system PATH." -ForegroundColor Red
}

Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green

# Run the Python application
try {
    & ".venv\Scripts\python.exe" "YouToMp3.py"
} catch {
    Write-Host "Error running application: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
