import sys
sys.path.insert(0, 'C:/Users/USER/.openclaw/workspace/scripts/trading')
from okx_trader import OKXTrader
import json

trader = OKXTrader(
    api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
    api_secret='4BF0777097F46740226B055B896D2CB1',
    passphrase='Abc32421.'
)

print("=" * 60)
print("Checking Funding Account Balance")
print("=" * 60)

# Get funding account balance
funding = trader.get_funding_balance()
print("\nFunding Account:")
print(json.dumps(funding, indent=2))

# Check if USDT is available
if funding.get('data'):
    usdt_balance = None
    for item in funding['data']:
        if item.get('ccy') == 'USDT':
            usdt_balance = item
            break
    
    if usdt_balance:
        avail = float(usdt_balance.get('availBal', 0))
        total = float(usdt_balance.get('bal', 0))
        print(f"\n[OK] USDT Found!")
        print(f"   Available: {avail} USDT")
        print(f"   Total: {total} USDT")
        
        if avail > 0:
            print(f"\n[Transferring] {avail} USDT to Trading Account...")
            result = trader.transfer_to_trading('USDT', avail)
            print(f"\nTransfer Result:")
            print(json.dumps(result, indent=2))
        else:
            print("\n[!] No available USDT to transfer")
    else:
        print("\n[X] No USDT found in Funding Account")
        print("\nOther currencies:")
        for item in funding['data'][:5]:
            print(f"   {item.get('ccy')}: {item.get('availBal', 0)}")
else:
    print("\n[X] Failed to get funding account balance")
    print(f"Error: {funding.get('msg', 'Unknown error')}")

# Check trading account balance again
print("\n" + "=" * 60)
print("Checking Trading Account Balance After Transfer")
print("=" * 60)
trading = trader.get_balance()
print(json.dumps(trading, indent=2)[:2000])
