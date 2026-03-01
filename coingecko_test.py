import requests
import json
from datetime import datetime

# CoinGecko API - 免费，无需 Key
BASE_URL = "https://api.coingecko.com/api/v3"

def get_btc_data():
    """获取 BTC 数据"""
    try:
        url = f"{BASE_URL}/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            market = data.get("market_data", {})
            return {
                "price": market.get("current_price", {}).get("usd", 0),
                "change_24h": market.get("price_change_percentage_24h", 0),
                "high_24h": market.get("high_24h", {}).get("usd", 0),
                "low_24h": market.get("low_24h", {}).get("usd", 0),
                "market_cap": market.get("market_cap", {}).get("usd", 0),
                "volume": market.get("total_volume", {}).get("usd", 0),
                "sentiment": market.get("sentiment_votes_up_percentage", 0)
            }
    except Exception as e:
        return {"error": str(e)}
    return None

def get_eth_data():
    """获取 ETH 数据"""
    try:
        url = f"{BASE_URL}/coins/ethereum?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            market = data.get("market_data", {})
            return {
                "price": market.get("current_price", {}).get("usd", 0),
                "change_24h": market.get("price_change_percentage_24h", 0),
                "high_24h": market.get("high_24h", {}).get("usd", 0),
                "low_24h": market.get("low_24h", {}).get("usd", 0),
                "market_cap": market.get("market_cap", {}).get("usd", 0),
                "volume": market.get("total_volume", {}).get("usd", 0)
            }
    except Exception as e:
        return {"error": str(e)}
    return None

def get_trending():
    """获取热搜币种"""
    try:
        url = f"{BASE_URL}/search/trending"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            coins = r.json().get("coins", [])
            return [c.get("item", {}).get("name") for c in coins[:5]]
    except Exception as e:
        return []
    return []

if __name__ == "__main__":
    print(f"=== CoinGecko Data {datetime.now().strftime('%H:%M')} ===\n")
    
    btc = get_btc_data()
    if btc and "error" not in btc:
        print(f"BTC: ${btc['price']:,.2f}")
        print(f"  24h Change: {btc['change_24h']:+.2f}%")
        print(f"  Market Cap: ${btc['market_cap']:,.0f}")
        print(f"  Volume: ${btc['volume']:,.0f}")
        if btc.get('sentiment'):
            print(f"  Community Sentiment: {btc['sentiment']:.1f}% Bullish")
    
    print()
    
    eth = get_eth_data()
    if eth and "error" not in eth:
        print(f"ETH: ${eth['price']:,.2f}")
        print(f"  24h Change: {eth['change_24h']:+.2f}%")
        print(f"  Market Cap: ${eth['market_cap']:,.0f}")
    
    trending = get_trending()
    if trending:
        print(f"\nTrending Coins: {', '.join(trending)}")
