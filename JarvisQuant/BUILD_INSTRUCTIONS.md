# Build Instructions for Jarvis Quant Trader

## Quick Build

### Option 1: Using Python Script (Recommended)
```bash
cd JarvisQuant
python build.py
```

### Option 2: Using Batch File (Windows)
```bash
cd JarvisQuant
build.bat
```

### Option 3: Manual Build
```bash
cd JarvisQuant
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --clean --onefile --windowed --name "JarvisQuantTrader" main.py
```

## Output

After successful build, the executable will be in:
```
JarvisQuant/dist/JarvisQuantTrader.exe
```

## Distribution

To share with others:

1. **Copy the dist folder:**
   ```
   dist/
   ├── JarvisQuantTrader.exe
   ├── config/
   │   └── api_config.json.example
   ├── Start_JarvisQuant.bat
   └── README.md
   ```

2. **Zip the dist folder:**
   ```bash
   zip -r JarvisQuantTrader-v1.0.zip dist/
   ```

3. **Share the zip file**

## Configuration

Users must:
1. Copy `config/api_config.json.example` to `config/api_config.json`
2. Edit `config/api_config.json` with their OKX API keys
3. Run `Start_JarvisQuant.bat` or `JarvisQuantTrader.exe`

## Requirements

- Windows 10/11
- No Python installation required (standalone executable)
- Internet connection for trading
