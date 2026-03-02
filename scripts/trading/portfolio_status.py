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
print("Portfolio Status - ETH + BTC")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Get all positions
positions = trader.get_positions()
total_pnl = 0
active_positions = []

if positions.get('data'):
    for pos in positions['data']:
        if float(pos.get('pos', 0)) != 0:
            symbol = pos.get('instId')
            side = 'LONG' if float(pos['pos']) > 0 else 'SHORT'
            size = abs(float(pos['pos']))
            entry = float(pos.get('avgPx', 0))
            upl = float(pos.get('upl', 0))
            total_pnl += upl
            active_positions.append({
                'symbol': symbol,
                'side': side,
                'size': size,
                'entry': entry,
                'pnl': upl
            })
            
            print(f"\n[{symbol}]")
            print(f"  Side: {side}")
            print(f"  Size: {size}")
            print(f"  Entry: ${entry:,.2f}")
            print(f"  PnL: ${upl:.4f} USDT")

if not active_positions:
    print("\n[NO ACTIVE POSITIONS]")

# Get balance
balance = trader.get_balance()
if balance.get('data') and balance['data'][0].get('details'):
    for detail in balance['data'][0]['details']:
        if detail.get('ccy') == 'USDT':
            eq = float(detail.get('eq', 0))
            avail = float(detail.get('availBal', 0))
            print(f"\n[ACCOUNT BALANCE]")
            print(f"  Total Equity: {eq:.2f} USDT")
            print(f"  Available: {avail:.2f} USDT")
            print(f"  Total Unrealized PnL: ${total_pnl:.4f} USDT")
            
            # Exposure
            exposed = eq - avail
            print(f"\n[EXPOSURE]")
            print(f"  Exposed: ${exposed:.2f} USDT ({(exposed/eq)*100:.1f}%)")
            print(f"  Available: ${avail:.2f} USDT ({(avail/eq)*100:.1f}%)")

print("\n" + "=" * 60)
print("Strategy: ETH + BTC Trend Following")
print("Max Position per trade: $20 USDT")
print("=" * 60)
