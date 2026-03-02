# Jarvis Quant Trader v1.0

Professional Cryptocurrency Trading Desktop Application

## Features

- **Real-time Price Charts**: Visualize ETH and BTC price movements
- **Automated Trading**: Trend-following strategy with risk management
- **Manual Trading**: Place orders manually with full control
- **Portfolio Management**: Track positions and PnL in real-time
- **Risk Controls**: Stop loss, take profit, and daily loss limits
- **Dark Theme**: Professional trading interface

## Installation

### Prerequisites
- Python 3.8 or higher
- OKX account with API access

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure API Keys
1. Copy the example configuration:
   ```bash
   cp config/api_config.json.example config/api_config.json
   ```

2. Edit `config/api_config.json` with your OKX API credentials:
   ```json
   {
       "api_key": "your_api_key",
       "api_secret": "your_api_secret",
       "passphrase": "your_passphrase"
   }
   ```

## Usage

### Run the Application
```bash
python main.py
```

### Build Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
```

## Trading Features

### Auto Trading
- Monitors ETH and BTC price trends
- Automatically enters positions on trend signals
- Manages stop loss and take profit
- Respects daily loss limits

### Manual Trading
- Place buy/sell orders manually
- Adjustable position size and leverage
- Quick close all positions button
- Real-time order status

### Risk Management
- Stop Loss: 2% (configurable)
- Take Profit: 6% (configurable)
- Daily Max Loss: 5%
- Position Size: Max $20 per trade

## Screenshots

[To be added]

## Warning

**Trading cryptocurrency involves substantial risk of loss.**
- Only trade with money you can afford to lose
- Past performance does not guarantee future results
- Always monitor your positions

## License

Proprietary Software - All Rights Reserved

## Support

For issues or questions, contact the developer.
