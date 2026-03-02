import sys
import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta

# Fix for Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okx_trader import OKXTrader

# Trading Configuration
CONFIG = {
    'capital': 71.73,
    'max_position_usd': 30,
    'leverage': 5,
    'stop_loss_pct': 0.02,
    'take_profit_pct': 0.06,
    'daily_max_loss_pct': 0.05,
    'symbols': ['ETH-USDT-SWAP', 'BTC-USDT-SWAP'],
    'timeframe': '4H',
    'check_interval': 300,
    'max_concurrent_positions': 3,
}

class AutoTradingBot:
    def __init__(self):
        self.trader = OKXTrader(
            api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
            api_secret='4BF0777097F46740226B055B896D2CB1',
            passphrase='Abc32421.'
        )
        self.daily_pnl = 0
        self.trades_today = 0
        self.today = datetime.now().date()
        self.active_position = None
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = "C:/Users/USER/.openclaw/workspace/logs/trading"
        os.makedirs(log_dir, exist_ok=True)
        log_file = f"{log_dir}/trading_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def reset_daily_stats(self):
        current_date = datetime.now().date()
        if current_date != self.today:
            self.logger.info(f"New day started. Resetting stats. Yesterday PnL: {self.daily_pnl:.2f}")
            self.daily_pnl = 0
            self.trades_today = 0
            self.today = current_date
            
    def check_breaker(self):
        daily_loss_limit = CONFIG['capital'] * CONFIG['daily_max_loss_pct']
        if self.daily_pnl <= -daily_loss_limit:
            self.logger.warning(f"[BREAKER] Daily loss limit reached: {self.daily_pnl:.2f} USDT")
            return True
        return False
        
    def get_klines(self, symbol, limit=20):
        try:
            url = f"https://www.okx.com/api/v5/market/history-candles?instId={symbol}&bar={CONFIG['timeframe']}&limit={limit}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data.get('code') == '0' and data.get('data'):
                candles = []
                for item in data['data']:
                    candles.append({
                        'timestamp': int(item[0]),
                        'open': float(item[1]),
                        'high': float(item[2]),
                        'low': float(item[3]),
                        'close': float(item[4]),
                        'volume': float(item[5])
                    })
                return candles
        except Exception as e:
            self.logger.error(f"Error fetching klines: {e}")
        return None
        
    def calculate_ma(self, candles, period):
        if len(candles) < period:
            return None
        closes = [c['close'] for c in candles[-period:]]
        return sum(closes) / len(closes)
        
    def get_signal(self, symbol):
        candles = self.get_klines(symbol)
        if not candles or len(candles) < 10:
            return None
            
        current_price = candles[-1]['close']
        ma5 = self.calculate_ma(candles, 5)
        ma10 = self.calculate_ma(candles, 10)
        
        if not ma5 or not ma10:
            return None
            
        if ma5 > ma10 * 1.002:
            trend = 'BULLISH'
        elif ma5 < ma10 * 0.998:
            trend = 'BEARISH'
        else:
            trend = 'NEUTRAL'
            
        return {
            'symbol': symbol,
            'price': current_price,
            'trend': trend,
            'ma5': ma5,
            'ma10': ma10,
            'timestamp': datetime.now().isoformat()
        }
        
    def get_position(self, symbol):
        try:
            positions = self.trader.get_positions()
            if positions.get('data'):
                for pos in positions['data']:
                    if pos.get('instId') == symbol and float(pos.get('pos', 0)) != 0:
                        return {
                            'symbol': symbol,
                            'side': 'long' if float(pos['pos']) > 0 else 'short',
                            'size': abs(float(pos['pos'])),
                            'entry_price': float(pos.get('avgPx', 0)),
                            'unrealized_pnl': float(pos.get('upl', 0)),
                            'leverage': float(pos.get('lever', 1))
                        }
        except Exception as e:
            self.logger.error(f"Error checking position: {e}")
        return None
        
    def calculate_position_size(self, symbol, price):
        position_value = min(CONFIG['max_position_usd'], CONFIG['capital'] * 0.25)
        size = position_value / price
        # OKX lot size handling
        if 'BTC' in symbol:
            # BTC lot size is 0.01
            size = round(size, 2)
            return max(size, 0.01)
        else:
            # ETH lot size is 0.01
            size = round(size, 2)
            return max(size, 0.01)
        
    def open_position(self, symbol, side, price):
        try:
            size = self.calculate_position_size(symbol, price)
            pos_side = 'long' if side == 'buy' else 'short'
            
            self.logger.info(f"[OPEN] {symbol} {side.upper()} {size} @ ${price:.2f}")
            
            result = self.trader.place_order(
                symbol=symbol,
                side=side,
                pos_side=pos_side,
                sz=size,
                ord_type='market'
            )
            
            if result.get('code') == '0' or result.get('simulated'):
                stop_loss = price * (1 - CONFIG['stop_loss_pct']) if side == 'buy' else price * (1 + CONFIG['stop_loss_pct'])
                take_profit = price * (1 + CONFIG['take_profit_pct']) if side == 'buy' else price * (1 - CONFIG['take_profit_pct'])
                
                self.active_position = {
                    'symbol': symbol,
                    'side': side,
                    'entry_price': price,
                    'size': size,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'opened_at': datetime.now().isoformat()
                }
                
                self.logger.info(f"[POSITION OPENED] SL: ${stop_loss:.2f} | TP: ${take_profit:.2f}")
                return True
            else:
                self.logger.error(f"[FAILED] Open position: {result}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error opening position: {e}")
            return False
            
    def close_position(self, symbol, reason):
        try:
            self.logger.info(f"[CLOSE] {symbol} - Reason: {reason}")
            result = self.trader.close_position(symbol)
            
            if result.get('code') == '0':
                if self.active_position:
                    self.trades_today += 1
                self.active_position = None
                self.logger.info("[POSITION CLOSED]")
                return True
            else:
                self.logger.error(f"[FAILED] Close position: {result}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
            return False
            
    def check_position_exit(self, position, current_price):
        if not self.active_position:
            return None, 0
            
        entry = self.active_position['entry_price']
        side = self.active_position['side']
        
        if side == 'buy':
            pnl_pct = (current_price - entry) / entry
        else:
            pnl_pct = (entry - current_price) / entry
            
        if pnl_pct <= -CONFIG['stop_loss_pct']:
            return 'STOP_LOSS', pnl_pct
            
        if pnl_pct >= CONFIG['take_profit_pct']:
            return 'TAKE_PROFIT', pnl_pct
            
        return None, pnl_pct
        
    def run_cycle(self):
        self.reset_daily_stats()
        
        if self.check_breaker():
            self.logger.info("[BREAKER ACTIVE] Trading halted for today")
            return
            
        symbol = CONFIG['symbols'][0]
        
        position = self.get_position(symbol)
        
        signal = self.get_signal(symbol)
        if not signal:
            self.logger.warning("[NO SIGNAL] Could not get market data")
            return
            
        current_price = signal['price']
        trend = signal['trend']
        
        self.logger.info(f"[MARKET] {symbol} @ ${current_price:.2f} | Trend: {trend}")
        
        if position:
            exit_reason, pnl_pct = self.check_position_exit(position, current_price)
            self.logger.info(f"[POSITION] {position['side'].upper()} | PnL: {pnl_pct*100:.2f}%")
            
            if exit_reason:
                self.daily_pnl += CONFIG['max_position_usd'] * pnl_pct
                self.close_position(symbol, exit_reason)
        else:
            self.logger.info("[NO POSITION] Looking for entry...")
            
            if trend == 'BULLISH':
                self.open_position(symbol, 'buy', current_price)
            elif trend == 'BEARISH':
                self.open_position(symbol, 'sell', current_price)
                
    def run(self):
        self.logger.info("=" * 70)
        self.logger.info("FULL AUTO TRADING BOT STARTED - ETH ONLY")
        self.logger.info(f"Capital: {CONFIG['capital']} USDT")
        self.logger.info("=" * 70)
        
        while True:
            try:
                self.run_cycle()
                self.logger.info(f"[SLEEP] {CONFIG['check_interval']}s...")
                time.sleep(CONFIG['check_interval'])
            except Exception as e:
                self.logger.error(f"[ERROR] {e}")
                time.sleep(60)

if __name__ == '__main__':
    bot = AutoTradingBot()
    bot.run()
