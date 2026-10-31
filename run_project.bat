@echo off
title Weather Data Analysis System - Launcher

echo =====================================================================
echo           WEATHER DATA ANALYSIS SYSTEM - AUTO LAUNCHER
echo =====================================================================
echo.

:: 1. Navigate to script directory
cd /d "%~dp0"
echo [1/4] Project folder: %cd%

:: 2. Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not found on your system PATH!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo [2/4] Detected %PYTHON_VER%

:: 3. Clear any old stuck processes on port 8501
echo [3/4] Ensuring port 8501 is ready...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8501" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

:: 4. Check and install dependencies if missing
python -c "import streamlit, pandas, matplotlib" >nul 2>&1
if errorlevel 1 (
    echo [!] Installing required packages from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install packages. Check internet connection.
        pause
        exit /b 1
    )
)

:: 5. Launch Streamlit Web Dashboard
echo [4/4] Starting Weather Data Analysis System...
echo.
echo =====================================================================
echo  Opening dashboard in your default browser...
echo  Local URL: http://localhost:8501
echo  To close the application, press Ctrl+C in this window.
echo =====================================================================
echo.

python -m streamlit run app.py

if errorlevel 1 (
    echo.
    echo Server closed or encountered an error.
    pause
)
