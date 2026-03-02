import sys
sys.path.insert(0, 'C:/Users/USER/.openclaw/workspace/scripts/trading')
from okx_trader import OKXTrader
import json
from datetime import datetime

trader = OKXTrader(
    api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
    api_secret='4BF0777097F46740226B055B896D2CB1',
    passphrase='Abc32421.'
)

print("=" * 60)
print("ETH Position Status")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Get current price
eth_ticker = trader.get_ticker('ETH-USDT-SWAP')
if eth_ticker.get('data'):
    current_price = float(eth_ticker['data'][0]['last'])
    print(f"\nCurrent ETH Price: ${current_price:.2f}")

# Get position
positions = trader.get_positions()
eth_position = None
if positions.get('data'):
    for pos in positions['data']:
        if pos.get('instId') == 'ETH-USDT-SWAP':
            eth_position = pos
            break

if eth_position and float(eth_position.get('pos', 0)) != 0:
    entry_price = float(eth_position.get('avgPx', 0))
    position_size = abs(float(eth_position.get('pos', 0)))
    side = 'LONG' if float(eth_position.get('pos', 0)) > 0 else 'SHORT'
    unrealized_pnl = float(eth_position.get('upl', 0))
    pnl_pct = (current_price - entry_price) / entry_price * 100 if side == 'LONG' else (entry_price - current_price) / entry_price * 100
    
    print(f"\n[ACTIVE POSITION]")
    print(f"Side: {side}")
    print(f"Entry Price: ${entry_price:.2f}")
    print(f"Position Size: {position_size} ETH")
    print(f"Current PnL: {unrealized_pnl:.4f} USDT ({pnl_pct:+.2f}%)")
    print(f"")
    print(f"Stop Loss: $2003.26 (-2% from entry)")
    print(f"Take Profit: $2166.79 (+6% from entry)")
    print(f"")
    print(f"Distance to SL: ${current_price - 2003.26:.2f}")
    print(f"Distance to TP: ${2166.79 - current_price:.2f}")
else:
    print("\n[NO ACTIVE POSITION]")
    print("Waiting for next entry signal...")

print("\n" + "=" * 60)
print("Strategy: ETH Trend Following Only")
print("BTC: DISABLED (will not trade)")
print("=" * 60)
