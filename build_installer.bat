@echo off
REM Video Editor - Windows Installer Build Script
REM Run this as Administrator for best results

echo ============================================
echo Video Editor - Windows Installer Builder
echo ============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo Python found.

REM Install PyInstaller if needed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Install NSIS if needed (via winget)
where makensis >nul 2>&1
if errorlevel 1 (
    echo NSIS not found. Installing via winget...
    winget install NSIS.NSIS
)

REM Run the build script
python build_installer.py

echo.
echo Build complete!
pause