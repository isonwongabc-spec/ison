#!/usr/bin/env python3
"""
最低成本自动交易 - 简单策略示例
策略: BTC 突破/跌破关键位时自动下单
"""
import requests
import json
import hmac
import hashlib
import base64
from datetime import datetime, timezone

# OKX API 配置
API_KEY = "112e3b78-387e-4df7-95ee-4f92f15d7d69"
API_SECRET = "4BF0777097F46740226B055B896D2CB1"
PASSPHRASE = "Abc32421."
BASE_URL = "https://www.okx.com"

class SimpleTrader:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.passphrase = PASSPHRASE
        
    def _sign(self, message):
        mac = hmac.new(self.api_secret.encode(), message.encode(), hashlib.sha256)
        return base64.b64encode(mac.digest()).decode()
    
    def _request(self, method, path, body=None):
        ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        msg = ts + method + path + (json.dumps(body) if body else '')
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': self._sign(msg),
            'OK-ACCESS-TIMESTAMP': ts,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        try:
            r = requests.request(method, BASE_URL + path, headers=headers, json=body)
            return r.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_price(self, coin="BTC"):
        """获取当前价格"""
        try:
            r = requests.get(f"{BASE_URL}/api/v5/market/ticker?instId={coin}-USDT-SWAP", timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get("code") == "0":
                    return float(data["data"][0]["last"])
        except:
            pass
        return None
    
    def place_order(self, coin, side, amount_usdt):
        """下单 - 市价单"""
        body = {
            "instId": f"{coin}-USDT-SWAP",
            "tdMode": "cross",  # 全仓模式
            "side": side,
            "ordType": "market",
            "sz": str(amount_usdt),  # USDT 金额
            "ccy": "USDT"
        }
        return self._request('POST', '/api/v5/trade/order', body)
    
    def check_strategy(self):
        """检查策略条件"""
        btc_price = self.get_price("BTC")
        if not btc_price:
            return "无法获取价格"
        
        print(f"[{datetime.now().strftime('%H:%M')}] BTC: ${btc_price:,.2f}")
        
        # 策略参数 - 可以修改
        BUY_PRICE = 65000    # 跌破此价买入
        SELL_PRICE = 70000   # 涨至此价卖出
        BUY_AMOUNT = 50      # 买入金额 (USDT)
        SELL_AMOUNT = 50     # 卖出金额 (USDT)
        
        if btc_price <= BUY_PRICE:
            print(f"触发买入条件! BTC <= ${BUY_PRICE}")
            result = self.place_order("BTC", "buy", BUY_AMOUNT)
            return f"买入订单: {json.dumps(result, indent=2)}"
        
        elif btc_price >= SELL_PRICE:
            print(f"触发卖出条件! BTC >= ${SELL_PRICE}")
            result = self.place_order("BTC", "sell", SELL_AMOUNT)
            return f"卖出订单: {json.dumps(result, indent=2)}"
        
        return f"未触发条件，继续监控 (买入<${BUY_PRICE}, 卖出>${SELL_PRICE})"

if __name__ == "__main__":
    trader = SimpleTrader()
    print("=" * 50)
    print("Simple Auto Trader - 最低版本")
    print("=" * 50)
    result = trader.check_strategy()
    print(result)
