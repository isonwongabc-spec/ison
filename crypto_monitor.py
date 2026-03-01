#!/usr/bin/env python3
"""
币圈数据监控 - OKX 数据源
"""
import requests
import json
from datetime import datetime

BASE_URL = "https://www.okx.com"

def get_price(coin="BTC"):
    """获取币种价格"""
    try:
        url = f"{BASE_URL}/api/v5/market/ticker?instId={coin}-USDT-SWAP"
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and r.json().get("code") == "0":
            d = r.json()["data"][0]
            return {
                "coin": coin,
                "price": float(d["last"]),
                "change_24h": round((float(d["last"]) - float(d["open24h"])) / float(d["open24h"]) * 100, 2),
                "high_24h": float(d["high24h"]),
                "low_24h": float(d["low24h"]),
                "volume": float(d["volCcy24h"])
            }
    except Exception as e:
        return {"error": str(e)}
    return None

def get_funding_rate(coin="BTC"):
    """获取资金费率"""
    try:
        url = f"{BASE_URL}/api/v5/public/funding-rate?instId={coin}-USDT-SWAP"
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and r.json().get("code") == "0":
            d = r.json()["data"][0]
            return {
                "coin": coin,
                "funding_rate": float(d["fundingRate"]) * 100,  # 转为百分比
                "next_funding_time": d["fundingTime"]
            }
    except Exception as e:
        return {"error": str(e)}
    return None

def get_open_interest(coin="BTC"):
    """获取持仓量"""
    try:
        url = f"{BASE_URL}/api/v5/public/open-interest?instType=SWAP&instId={coin}-USDT-SWAP"
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and r.json().get("code") == "0":
            d = r.json()["data"][0]
            return {
                "coin": coin,
                "oi": float(d["oi"]),
                "oi_usd": float(d["oiCcy"])
            }
    except Exception as e:
        return {"error": str(e)}
    return None

def market_report():
    """生成市场报告"""
    coins = ["BTC", "ETH"]
    report = []
    
    for coin in coins:
        price_data = get_price(coin)
        funding_data = get_funding_rate(coin)
        
        if price_data and "error" not in price_data:
            line = f"{coin}: ${price_data['price']:,.2f} ({price_data['change_24h']:+.2f}%)"
            if funding_data and "error" not in funding_data:
                fr = funding_data["funding_rate"]
                sentiment = "Bullish" if fr > 0.01 else "Bearish" if fr < -0.01 else "Neutral"
                line += f" | Funding: {fr:.4f}% ({sentiment})"
            report.append(line)
    
    return "\n".join(report) if report else "Data fetch failed"

if __name__ == "__main__":
    print(f"=== Crypto Monitor {datetime.now().strftime('%H:%M')} ===\n")
    print(market_report())
