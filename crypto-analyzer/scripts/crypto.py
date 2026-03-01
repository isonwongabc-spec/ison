#!/usr/bin/env python3
"""
加密货币分析脚本
依赖: requests
"""

import argparse
import sys
import subprocess


def ensure_requests():
    """确保 requests 已安装"""
    try:
        import requests
    except ImportError:
        print("正在安装 requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=True)


def get_crypto_price(symbol):
    """获取加密货币价格"""
    import requests
    
    # CoinGecko API (免费，无需API Key)
    symbol = symbol.lower()
    
    # 映射常见币种
    coin_ids = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'sol': 'solana',
        'ada': 'cardano',
        'doge': 'dogecoin',
        'xrp': 'ripple',
        'dot': 'polkadot',
        'avax': 'avalanche-2',
        'bnb': 'binancecoin',
        'matic': 'matic-network'
    }
    
    coin_id = coin_ids.get(symbol, symbol)
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'error' in data:
            return None
        
        return {
            'name': data.get('name', symbol.upper()),
            'symbol': data.get('symbol', symbol).upper(),
            'current_price': data['market_data']['current_price']['usd'],
            'price_change_24h': data['market_data']['price_change_percentage_24h'],
            'price_change_7d': data['market_data']['price_change_percentage_7d'],
            'market_cap': data['market_data']['market_cap']['usd'],
            'volume_24h': data['market_data']['total_volume']['usd'],
            'high_24h': data['market_data']['high_24h']['usd'],
            'low_24h': data['market_data']['low_24h']['usd'],
            'ath': data['market_data']['ath']['usd'],  # 历史最高价
            'atl': data['market_data']['atl']['usd'],  # 历史最低价
        }
    except Exception as e:
        print(f"获取 {symbol.upper()} 数据失败: {e}")
        return None


def analyze_crypto(symbol):
    """分析单个加密货币"""
    data = get_crypto_price(symbol)
    
    if not data:
        return
    
    print(f"\n{'='*50}")
    print(f"💎 {data['name']} ({data['symbol']})")
    print(f"{'='*50}")
    
    # 价格
    price = data['current_price']
    if price >= 1000:
        price_str = f"${price:,.2f}"
    else:
        price_str = f"${price:,.4f}"
    
    change_24h = data['price_change_24h'] or 0
    change_7d = data['price_change_7d'] or 0
    
    change_emoji_24h = "🟢" if change_24h >= 0 else "🔴"
    change_emoji_7d = "🟢" if change_7d >= 0 else "🔴"
    
    print(f"💰 当前价格: {price_str}")
    print(f"   {change_emoji_24h} 24h: {change_24h:+.2f}%")
    print(f"   {change_emoji_7d} 7d:  {change_7d:+.2f}%")
    
    # 24h高低
    print(f"\n📊 24小时")
    print(f"   最高: ${data['high_24h']:,.2f}")
    print(f"   最低: ${data['low_24h']:,.2f}")
    
    # 历史高低
    print(f"\n🏔️ 历史价格")
    print(f"   ATH: ${data['ath']:,.2f}")
    print(f"   ATL: ${data['atl']:,.6f}")
    
    # 市值和成交量
    print(f"\n📈 市场数据")
    print(f"   市值: ${data['market_cap']:,.0f}")
    print(f"   24h成交量: ${data['volume_24h']:,.0f}")
    
    # 距ATH跌幅
    ath_drop = (data['current_price'] - data['ath']) / data['ath'] * 100
    print(f"\n📉 距历史最高: {ath_drop:.1f}%")


def main():
    parser = argparse.ArgumentParser(description="加密货币分析")
    parser.add_argument("symbols", nargs="+", help="币种代码 (如: BTC ETH)")
    
    args = parser.parse_args()
    
    ensure_requests()
    
    for symbol in args.symbols:
        analyze_crypto(symbol)
    
    print(f"\n{'='*50}")
    print("⚠️ 仅供参考，不构成投资建议")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
