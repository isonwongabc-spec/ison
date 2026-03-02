# Quantitative Trading Bot

Automated cryptocurrency trading bot for ETH and BTC using trend-following strategy.

## Features

- **Dual Symbol Trading**: ETH and BTC
- **Trend Following**: MA5/MA10 crossover strategy
- **Risk Management**: 
  - Stop Loss: 2%
  - Take Profit: 6%
  - Daily Max Loss: 5%
  - Position Size: Max $20 per trade
- **Auto Execution**: Checks market every 5 minutes

## Setup

1. Copy configuration template:
   ```bash
   cp config/okx-trading.env.example config/okx-trading.env
   ```

2. Edit `config/okx-trading.env` with your OKX API credentials:
   ```
   API_KEY=your_actual_api_key
   API_SECRET=your_actual_api_secret
   API_PASSPHRASE=your_actual_passphrase
   ```

3. Install dependencies:
   ```bash
   pip install requests
   ```

4. Run the bot:
   ```bash
   python scripts/trading/auto_trader_v2.py
   ```

## Trading Strategy

### Entry Conditions
- **Bullish Signal**: MA5 > MA10 (Long)
- **Bearish Signal**: MA5 < MA10 (Short)

### Exit Conditions
- Stop Loss: -2% from entry
- Take Profit: +6% from entry
- Daily Loss Limit: -5% (circuit breaker)

## Risk Warning

⚠️ **Trading cryptocurrency involves substantial risk of loss.**
- Only trade with money you can afford to lose
- Past performance does not guarantee future results
- The bot can and will lose money

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| INITIAL_CAPITAL | 70 | Starting capital in USDT |
| MAX_LEVERAGE | 3 | Maximum leverage multiplier |
| STOP_LOSS_PERCENT | 2 | Stop loss percentage |
| TAKE_PROFIT_PERCENT | 6 | Take profit percentage |
| MAX_POSITION_SIZE_USD | 20 | Maximum position size per trade |

## License

Private use only.
