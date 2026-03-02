#!/usr/bin/env python3
"""
Full Auto Trading Bot for Boss
Strategy: Trend Following with Risk Management
"""

import sys
import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okx_trader import OKXTrader

# Trading Configuration
CONFIG = {
    'capital': 71.73,
    'max_position_usd': 20,
    'leverage': 3,
    'stop_loss_pct': 0.02,
    'take_profit_pct': 0.06,
    'daily_max_loss_pct': 0.05,
    'symbols': ['ETH-USDT-SWAP'],
    'timeframe': '4H',
    'check_interval': 300,  # 5 minutes
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
                logging.StreamHandler()
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
        """Get recent price data"""
        try:
            url = f"https://www.okx.com/api/v5/market/history-candles?instId={symbol}&bar={CONFIG['timeframe']}&limit={limit}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data.get('code') == '0' and data.get('data'):
                # Format: [ts, o, h, l, c, vol, volCcy]
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
        """Calculate moving average"""
        if len(candles) < period:
            return None
        closes = [c['close'] for c in candles[-period:]]
        return sum(closes) / len(closes)
        
    def get_signal(self, symbol):
        """Generate trading signal based on MA crossover"""
        candles = self.get_klines(symbol)
        if not candles or len(candles) < 10:
            return None
            
        current_price = candles[-1]['close']
        ma5 = self.calculate_ma(candles, 5)
        ma10 = self.calculate_ma(candles, 10)
        
        if not ma5 or not ma10:
            return None
            
        # Determine trend
        if ma5 > ma10 * 1.002:  # 0.2% buffer to avoid noise
            trend = 'BULLISH'
        elif ma5 < ma10 * 0.998:
            trend = 'BEARISH'
        else:
            trend = 'NEUTRAL'
            
        # Calculate volatility (ATR-like)
        highs = [c['high'] for c in candles[-5:]]
        lows = [c['low'] for c in candles[-5:]]
        avg_range = sum([h-l for h, l in zip(highs, lows)]) / len(highs)
        volatility = avg_range / current_price
        
        return {
            'symbol': symbol,
            'price': current_price,
            'trend': trend,
            'ma5': ma5,
            'ma10': ma10,
            'volatility': volatility,
            'timestamp': datetime.now().isoformat()
        }
        
    def get_position(self, symbol):
        """Check if we have an open position"""
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
        
    def calculate_position_size(self, price):
        """Calculate position size"""
        position_value = min(CONFIG['max_position_usd'], CONFIG['capital'] * 0.25)
        size = position_value / price
        return round(size, 4)
        
    def open_position(self, symbol, side, price):
        """Open a new position"""
        try:
            size = self.calculate_position_size(price)
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
        """Close current position"""
        try:
            self.logger.info(f"[CLOSE] {symbol} - Reason: {reason}")
            result = self.trader.close_position(symbol)
            
            if result.get('code') == '0':
                # Estimate PnL (actual will be in next balance check)
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
        """Check if position should be closed"""
        if not self.active_position:
            return False
            
        entry = self.active_position['entry_price']
        side = self.active_position['side']
        
        # Calculate unrealized PnL
        if side == 'buy':  # Long
            pnl_pct = (current_price - entry) / entry
        else:  # Short
            pnl_pct = (entry - current_price) / entry
            
        # Check stop loss
        if pnl_pct <= -CONFIG['stop_loss_pct']:
            return 'STOP_LOSS', pnl_pct
            
        # Check take profit
        if pnl_pct >= CONFIG['take_profit_pct']:
            return 'TAKE_PROFIT', pnl_pct
            
        return None, pnl_pct
        
    def run_cycle(self):
        """Run one trading cycle"""
        self.reset_daily_stats()
        
        if self.check_breaker():
            self.logger.info("[BREAKER ACTIVE] Trading halted for today")
            return
            
        symbol = CONFIG['symbols'][0]  # ETH only for now
        
        # Get current position
        position = self.get_position(symbol)
        
        # Get market data
        signal = self.get_signal(symbol)
        if not signal:
            self.logger.warning("[NO SIGNAL] Could not get market data")
            return
            
        current_price = signal['price']
        trend = signal['trend']
        
        self.logger.info(f"[MARKET] {symbol} @ ${current_price:.2f} | Trend: {trend} | MA5: ${signal['ma5']:.2f} | MA10: ${signal['ma10']:.2f}")
        
        # If we have a position, check exit conditions
        if position:
            exit_reason, pnl_pct = self.check_position_exit(position, current_price)
            self.logger.info(f"[POSITION] {position['side'].upper()} | Entry: ${position['entry_price']:.2f} | PnL: {pnl_pct*100:.2f}%")
            
            if exit_reason:
                self.daily_pnl += CONFIG['max_position_usd'] * pnl_pct
                self.close_position(symbol, exit_reason)
            else:
                # Check if trend reversed
                if (position['side'] == 'long' and trend == 'BEARISH') or \
                   (position['side'] == 'short' and trend == 'BULLISH'):
                    # Optional: Close on trend reversal (can be disabled)
                    pass
                    
        else:
            # No position - check entry conditions
            self.logger.info(f"[NO POSITION] Looking for entry...")
            
            if trend == 'BULLISH':
                self.open_position(symbol, 'buy', current_price)
            elif trend == 'BEARISH':
                self.open_position(symbol, 'sell', current_price)
                
    def run(self):
        """Main loop"""
        self.logger.info("=" * 70)
        self.logger.info("FULL AUTO TRADING BOT STARTED")
        self.logger.info(f"Capital: {CONFIG['capital']} USDT | Max Position: {CONFIG['max_position_usd']} USDT")
        self.logger.info(f"Leverage: {CONFIG['leverage']}x | SL: {CONFIG['stop_loss_pct']*100}% | TP: {CONFIG['take_profit_pct']*100}%")
        self.logger.info("=" * 70)
        
        while True:
            try:
                self.run_cycle()
                self.logger.info(f"[SLEEP] Next check in {CONFIG['check_interval']} seconds...")
                time.sleep(CONFIG['check_interval'])
            except Exception as e:
                self.logger.error(f"[ERROR] {e}")
                time.sleep(60)

if __name__ == '__main__':
    bot = AutoTradingBot()
    bot.run()
