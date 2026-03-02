@echo off
chcp 65001 >nul
echo ==========================================
echo Jarvis Quant Trader - Build Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/5] Building executable...
pyinstaller --clean --onefile --windowed --name "JarvisQuantTrader" --icon=NONE main.py
if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo.
echo [4/5] Copying configuration files...
if not exist "dist\config" mkdir "dist\config"
copy "config\*.example" "dist\config\" >nul 2>&1
copy "README.md" "dist\" >nul 2>&1

echo.
echo [5/5] Creating startup script...
echo @echo off > "dist\Start_JarvisQuant.bat"
echo chcp 65001 ^>nul >> "dist\Start_JarvisQuant.bat"
echo echo Starting Jarvis Quant Trader... >> "dist\Start_JarvisQuant.bat"
echo JarvisQuantTrader.exe >> "dist\Start_JarvisQuant.bat"

echo.
echo ==========================================
echo Build completed successfully!
echo ==========================================
echo.
echo Output: dist\JarvisQuantTrader.exe
echo.
echo To run the application:
echo   1. Copy config\api_config.json.example to config\api_config.json
echo   2. Edit config\api_config.json with your API keys
echo   3. Double-click dist\JarvisQuantTrader.exe
echo.
pause
