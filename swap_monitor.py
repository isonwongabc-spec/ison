#!/usr/bin/env python3
"""
合约(SWAP)专用监控系统 - OKX
监控: 资金费率、持仓量、爆仓数据、多空比
"""
import requests
import json
from datetime import datetime

BASE_URL = "https://www.okx.com"

class SwapMonitor:
    def __init__(self):
        self.coins = ["BTC", "ETH", "SOL", "XRP", "DOGE"]
    
    def _request(self, path):
        try:
            r = requests.get(f"{BASE_URL}{path}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                return data if data.get("code") == "0" else None
        except:
            pass
        return None
    
    def get_funding_rate(self, coin):
        """资金费率 - 关键指标"""
        data = self._request(f"/api/v5/public/funding-rate?instId={coin}-USDT-SWAP")
        if data and data.get("data"):
            d = data["data"][0]
            fr = float(d["fundingRate"]) * 100
            return {
                "coin": coin,
                "rate": fr,
                "next_time": d["fundingTime"],
                "sentiment": "Bullish" if fr > 0.01 else "Bearish" if fr < -0.01 else "Neutral"
            }
        return None
    
    def get_open_interest(self, coin):
        """持仓量 - 市场热度"""
        data = self._request(f"/api/v5/public/open-interest?instType=SWAP&instId={coin}-USDT-SWAP")
        if data and data.get("data"):
            d = data["data"][0]
            return {
                "coin": coin,
                "oi": float(d["oi"]),
                "oi_usd": float(d["oiCcy"])
            }
        return None
    
    def get_liquidation(self, coin, limit=100):
        """爆仓数据 - 市场极端情绪"""
        # OKX liquidation fills
        data = self._request(f"/api/v5/public/liquidation-orders?instType=SWAP&mgnMode= liquidate&instId={coin}-USDT-SWAP&limit={limit}")
        if data and data.get("data"):
            long_liq = sum(float(x["sz"]) for x in data["data"] if x["side"] == "long")
            short_liq = sum(float(x["sz"]) for x in data["data"] if x["side"] == "short")
            return {
                "coin": coin,
                "long_liq": long_liq,
                "short_liq": short_liq,
                "total": long_liq + short_liq,
                "dominant": "多头爆仓" if long_liq > short_liq else "空头爆仓"
            }
        return None
    
    def get_price(self, coin):
        """价格数据"""
        data = self._request(f"/api/v5/market/ticker?instId={coin}-USDT-SWAP")
        if data and data.get("data"):
            d = data["data"][0]
            return {
                "coin": coin,
                "price": float(d["last"]),
                "change_24h": round((float(d["last"]) - float(d["open24h"])) / float(d["open24h"]) * 100, 2),
                "high": float(d["high24h"]),
                "low": float(d["low24h"]),
                "volume": float(d["volCcy24h"])
            }
        return None
    
    def full_report(self):
        """完整报告"""
        report = []
        report.append(f"=== SWAP Monitor Report {datetime.now().strftime('%H:%M')} ===\n")
        
        for coin in self.coins:
            price = self.get_price(coin)
            funding = self.get_funding_rate(coin)
            oi = self.get_open_interest(coin)
            
            if price:
                line = f"{coin}: ${price['price']:,.2f} ({price['change_24h']:+.2f}%)"
                if funding:
                    fr = funding['rate']
                    emoji = "LONG" if fr > 0.01 else "SHORT" if fr < -0.01 else "NEUTRAL"
                    line += f" | {emoji} Fund: {fr:.4f}%"
                if oi:
                    line += f" | OI: ${oi['oi_usd']:,.0f}"
                report.append(line)
        
        return "\n".join(report)

if __name__ == "__main__":
    monitor = SwapMonitor()
    print(monitor.full_report())
