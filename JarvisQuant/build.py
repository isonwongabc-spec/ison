#!/usr/bin/env python3
"""
Build script for Jarvis Quant Trader
Creates a standalone executable using PyInstaller
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"[STEP] {description}")
    print('='*60)
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode != 0:
        print(f"[ERROR] {description} failed!")
        return False
    print(f"[OK] {description} completed!")
    return True

def main():
    print("="*60)
    print("Jarvis Quant Trader - Build Script")
    print("="*60)
    
    # Get current directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return 1
    
    # Step 2: Install PyInstaller
    if not run_command("pip install pyinstaller", "Installing PyInstaller"):
        return 1
    
    # Step 3: Clean previous builds
    print("\n[STEP] Cleaning previous builds...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")
    
    # Step 4: Build executable
    build_cmd = (
        "pyinstaller "
        "--clean "
        "--onefile "
        "--windowed "
        "--name \"JarvisQuantTrader\" "
        "--add-data \"config;config\" "
        "--hidden-import PyQt6.sip "
        "--hidden-import PyQt6.QtCharts "
        "--hidden-import requests "
        "--hidden-import urllib3 "
        "--hidden-import charset_normalizer "
        "--hidden-import certifi "
        "--hidden-import idna "
        "main.py"
    )
    
    if not run_command(build_cmd, "Building executable"):
        return 1
    
    # Step 5: Copy additional files
    print("\n[STEP] Copying configuration files...")
    os.makedirs("dist/config", exist_ok=True)
    
    for file in Path("config").glob("*.example"):
        shutil.copy(file, f"dist/config/{file.name}")
        print(f"  Copied {file.name}")
    
    if os.path.exists("README.md"):
        shutil.copy("README.md", "dist/README.md")
        print("  Copied README.md")
    
    # Step 6: Create startup script
    print("\n[STEP] Creating startup scripts...")
    
    # Windows batch file
    with open("dist/Start_JarvisQuant.bat", "w") as f:
        f.write("@echo off\n")
        f.write("chcp 65001 >nul\n")
        f.write("echo ==========================================\n")
        f.write("echo Jarvis Quant Trader v1.0\n")
        f.write("echo ==========================================\n")
        f.write("echo.\n")
        f.write("echo Starting...\n")
        f.write("start JarvisQuantTrader.exe\n")
    
    # PowerShell script
    with open("dist/Start_JarvisQuant.ps1", "w") as f:
        f.write("# Jarvis Quant Trader Startup Script\n")
        f.write("Write-Host '==========================================' -ForegroundColor Cyan\n")
        f.write("Write-Host 'Jarvis Quant Trader v1.0' -ForegroundColor Cyan\n")
        f.write("Write-Host '==========================================' -ForegroundColor Cyan\n")
        f.write("Write-Host ''\n")
        f.write("Write-Host 'Starting application...' -ForegroundColor Green\n")
        f.write(".\\JarvisQuantTrader.exe\n")
    
    print("  Created Start_JarvisQuant.bat")
    print("  Created Start_JarvisQuant.ps1")
    
    # Success message
    print("\n" + "="*60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nOutput files:")
    print("  [EXE] dist/JarvisQuantTrader.exe  (Main application)")
    print("  [CFG] dist/config/                 (Configuration files)")
    print("  [BAT] dist/Start_JarvisQuant.bat   (Quick start script)")
    print("\nTo distribute:")
    print("  1. Zip the entire 'dist' folder")
    print("  2. Share the zip file")
    print("  3. Users extract and run Start_JarvisQuant.bat")
    print("\nNote: Users need to configure API keys in config/api_config.json")
    print("="*60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
