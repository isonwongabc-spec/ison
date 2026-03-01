#!/usr/bin/env python3
import requests
from datetime import datetime

BASE_URL = 'https://www.okx.com'
coins = ['BTC', 'ETH']

print(f'=== 合约深度分析 {datetime.now().strftime("%H:%M")} ===\n')

for coin in coins:
    try:
        # 价格和24h数据
        r1 = requests.get(f'{BASE_URL}/api/v5/market/ticker?instId={coin}-USDT-SWAP', timeout=10)
        # 资金费率
        r2 = requests.get(f'{BASE_URL}/api/v5/public/funding-rate?instId={coin}-USDT-SWAP', timeout=10)
        # 持仓量
        r3 = requests.get(f'{BASE_URL}/api/v5/public/open-interest?instType=SWAP&instId={coin}-USDT-SWAP', timeout=10)
        
        if r1.status_code == 200 and r2.status_code == 200:
            p = r1.json()['data'][0]
            f = r2.json()['data'][0]
            
            price = float(p['last'])
            change = round((price - float(p['open24h'])) / float(p['open24h']) * 100, 2)
            high = float(p['high24h'])
            low = float(p['low24h'])
            vol = float(p['volCcy24h'])
            fr = float(f['fundingRate']) * 100
            
            print(f'{coin}-USDT-SWAP:')
            print(f'  Price: ${price:,.2f} ({change:+.2f}%)')
            print(f'  24h Range: ${low:,.2f} - ${high:,.2f}')
            print(f'  Volatility: {round((high-low)/low*100, 2)}%')
            print(f'  24h Volume: ${vol:,.0f}')
            print(f'  Funding Rate: {fr:.4f}%')
            
            if r3.status_code == 200:
                oi = r3.json()['data'][0]
                print(f'  Open Interest: ${float(oi["oiCcy"]):,.0f}')
            
            # 合约交易信号
            print(f'  Signal: ', end='')
            if fr > 0.01:
                print('Longs pay funding - Bullish bias')
            elif fr < -0.01:
                print('Shorts pay funding - Bearish bias')
            else:
                print('Neutral funding - Balanced')
            print()
    except Exception as e:
        print(f'{coin} Error: {e}')

print('=== 合约交易建议 ===')
print('BTC: 4h内高点$66,660, 低点$63,020 - 区间操作')
print('ETH: 关注$2,000整数关口阻力')
