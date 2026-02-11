@echo off
REM Production Startup Script for Tenant Management System (Windows)
REM This script starts the application with production settings

echo ================================================================
echo     Tenant Management System - Production Startup (Windows)
echo ================================================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Creating from .env.example...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [OK] Created .env file
        echo [!] Please edit .env file with your settings before continuing
        echo.
        pause
        notepad .env
    ) else (
        echo [ERROR] .env.example not found
        pause
        exit /b 1
    )
)

REM Check Python
echo [INFO] Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

REM Check dependencies
echo [INFO] Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies not installed
    set /p INSTALL="Install now? (Y/n): "
    if /i "%INSTALL%" neq "n" (
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo [ERROR] Failed to install dependencies
            pause
            exit /b 1
        )
        echo [OK] Dependencies installed
    ) else (
        echo [ERROR] Cannot start without dependencies
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependencies OK
)

REM Create directories
echo [INFO] Creating directories...
if not exist "data" mkdir data
if not exist "static\qrcodes" mkdir static\qrcodes
if not exist "backups" mkdir backups
if not exist "logs" mkdir logs
echo [OK] Directories ready

REM Create backup
if exist "data\tenants.db" (
    echo [INFO] Creating backup...
    set BACKUP_FILE=backups\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db
    copy "data\tenants.db" "%BACKUP_FILE%" >nul
    echo [OK] Backup created
)

REM Check if already running
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Port 5000 is already in use
    echo Another instance may be running
    set /p KILL="Kill existing process and continue? (y/N): "
    if /i "%KILL%"=="y" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
            taskkill /PID %%a /F >nul 2>&1
        )
        timeout /t 2 /nobreak >nul
        echo [OK] Existing process killed
    ) else (
        echo [ERROR] Cannot start - port in use
        pause
        exit /b 1
    )
)

echo.
echo ================================================================
echo                Starting Application...
echo ================================================================
echo.
echo [INFO] Access the application at:
echo   - Local: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start application
python app.py

REM Cleanup
echo.
echo Application stopped
pause
