import sys
sys.path.insert(0, 'C:/Users/USER/.openclaw/workspace/scripts/trading')
from okx_trader import OKXTrader
import json

trader = OKXTrader(
    api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
    api_secret='4BF0777097F46740226B055B896D2CB1',
    passphrase='Abc32421.'
)

print("Account Balance Check")
print("=" * 60)

balance = trader.get_balance()
if balance.get('data') and balance['data'][0].get('details'):
    for detail in balance['data'][0]['details']:
        ccy = detail.get('ccy')
        eq = float(detail.get('eq', 0))
        avail = float(detail.get('availBal', 0))
        upl = detail.get('upl', '0')
        
        if ccy == 'USDT' and eq > 0:
            print(f"\nUSDT Balance:")
            print(f"  Total Equity: {eq:.2f} USDT")
            print(f"  Available: {avail:.2f} USDT")
            print(f"  Unrealized PnL: {upl}")
            
            # Compare with initial
            initial = 71.73
            change = eq - initial
            print(f"\n  Initial: {initial:.2f} USDT")
            print(f"  Current: {eq:.2f} USDT")
            print(f"  Change: {change:+.2f} USDT ({(change/initial)*100:+.2f}%)")
