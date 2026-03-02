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
print("BTC Market Analysis")
print("=" * 60)

# Get BTC current price
btc_ticker = trader.get_ticker('BTC-USDT-SWAP')
if btc_ticker.get('data'):
    btc = btc_ticker['data'][0]
    current_price = float(btc['last'])
    open_24h = float(btc['open24h'])
    high_24h = float(btc['high24h'])
    low_24h = float(btc['low24h'])
    change_24h = ((current_price - open_24h) / open_24h) * 100
    
    print(f"\nCurrent Price: ${current_price:,.2f}")
    print(f"24h Change: {change_24h:+.2f}%")
    print(f"24h High: ${high_24h:,.2f}")
    print(f"24h Low: ${low_24h:,.2f}")
    print(f"24h Range: ${high_24h - low_24h:,.2f} ({((high_24h-low_24h)/low_24h)*100:.2f}%)")

# Calculate position size based on current strategy
position_value = 20  # USDT
leverage = 3
btc_position_size = position_value / current_price

print("\n" + "=" * 60)
print("BTC Trading Parameters (Same Strategy)")
print("=" * 60)
print(f"Capital Allocation: 20 USDT (28% of 71.73 USDT)")
print(f"Leverage: {leverage}x")
print(f"Position Size: {btc_position_size:.6f} BTC")
print(f"Notional Value: ${position_value * leverage:.2f} USDT")
print(f"")
print(f"Stop Loss: {current_price * 0.98:,.2f} (-2%)")
print(f"Take Profit: {current_price * 1.06:,.2f} (+6%)")
print(f"")
print(f"Risk per trade: ${position_value * 0.02:.2f} USDT")
print(f"Potential profit: ${position_value * 0.06:.2f} USDT")
print(f"Risk/Reward: 1:3")

print("\n" + "=" * 60)
print("Combined Portfolio (ETH + BTC)")
print("=" * 60)
print(f"ETH Position: 18 USDT (already open)")
print(f"BTC Position: 20 USDT (available)")
print(f"Total Exposed: 38 USDT (53% of capital)")
print(f"Reserved Cash: 33.73 USDT (47% of capital)")
print(f"")
print(f"Note: Trading both increases diversification")
print(f"      but also increases correlation risk")
