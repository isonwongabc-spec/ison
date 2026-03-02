#!/usr/bin/env python3
"""
Quantitative Trading Bot for Boss
Strategy: Trend Following + Grid Defense
"""

import sys
import os
import json
import time
from datetime import datetime
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okx_trader import OKXTrader

# Configuration
CONFIG = {
    'capital': 70,  # USDT
    'max_leverage': 3,
    'stop_loss_pct': 0.02,  # 2%
    'take_profit_pct': 0.06,  # 6%
    'daily_max_loss_pct': 0.05,  # 5%
    'symbols': ['ETH-USDT-SWAP', 'BTC-USDT-SWAP'],
    'timeframe': '4H',
    'check_interval': 900,  # 15 minutes
}

class TradingBot:
    def __init__(self):
        self.trader = OKXTrader(
            api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
            api_secret='4BF0777097F46740226B055B896D2CB1',
            passphrase='Abc32421.'
        )
        self.daily_pnl = 0
        self.trades_today = 0
        self.positions = {}
        self.setup_logging()
    
    def setup_logging(self):
        log_file = f"C:/Users/USER/.openclaw/workspace/logs/trading/trading_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_breaker(self):
        """Check if daily loss limit reached"""
        daily_loss_limit = CONFIG['capital'] * CONFIG['daily_max_loss_pct']
        if abs(self.daily_pnl) >= daily_loss_limit:
            self.logger.warning(f"🚫 DAILY LOSS LIMIT REACHED: {self.daily_pnl:.2f} USDT")
            return True
        return False
    
    def get_signal(self, symbol):
        """Get trading signal based on 4H breakout"""
        # This is a simplified version - in production, fetch actual kline data
        ticker = self.trader.get_ticker(symbol)
        if ticker.get('data'):
            current_price = float(ticker['data'][0]['last'])
            return {
                'symbol': symbol,
                'price': current_price,
                'signal': 'NEUTRAL',  # Will be implemented with actual strategy
                'timestamp': datetime.now().isoformat()
            }
        return None
    
    def calculate_position_size(self, confidence):
        """Calculate position size based on confidence and risk"""
        risk_per_trade = CONFIG['capital'] * 0.02  # 2% risk
        position_size = risk_per_trade * CONFIG['max_leverage']
        return min(position_size, 10)  # Max 10 USDT per trade
    
    def run(self):
        """Main trading loop"""
        self.logger.info("=" * 60)
        self.logger.info("🚀 Trading Bot Started")
        self.logger.info(f"💰 Capital: {CONFIG['capital']} USDT")
        self.logger.info(f"📊 Max Leverage: {CONFIG['max_leverage']}x")
        self.logger.info("=" * 60)
        
        # Test connection
        balance = self.trader.get_balance()
        self.logger.info(f"Account connected. Balance data received.")
        
        while True:
            try:
                # Check breaker
                if self.check_breaker():
                    self.logger.info("Trading halted for today. Will resume tomorrow.")
                    time.sleep(3600)  # Sleep 1 hour
                    continue
                
                # Get signals for all symbols
                for symbol in CONFIG['symbols']:
                    signal = self.get_signal(symbol)
                    if signal:
                        self.logger.info(f"📈 {symbol}: ${signal['price']:.2f} | Signal: {signal['signal']}")
                
                # Check every 15 minutes
                self.logger.info(f"💤 Sleeping for {CONFIG['check_interval']} seconds...")
                time.sleep(CONFIG['check_interval'])
                
            except Exception as e:
                self.logger.error(f"❌ Error in trading loop: {e}")
                time.sleep(60)

if __name__ == '__main__':
    bot = TradingBot()
    
    # For testing, just run one iteration
    print("Testing trading bot initialization...")
    balance = bot.trader.get_balance()
    print(f"Balance response: {json.dumps(balance, indent=2)[:500]}")
    
    # Uncomment to run continuous trading
    # bot.run()
