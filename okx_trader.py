#!/usr/bin/env python3
"""OKX Auto Trader - Usage: python okx_trader.py --action balance|price|order"""
import hmac, hashlib, base64, json, argparse
from datetime import datetime, timezone
import requests

API_KEY = "112e3b78-387e-4df7-95ee-4f92f15d7d69"
API_SECRET = "4BF0777097F46740226B055B896D2CB1"
PASSPHRASE = "Abc32421."
BASE_URL = "https://www.okx.com"

class OKXTrader:
    def _ts(self):
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def _sign(self, msg):
        mac = hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256)
        return base64.b64encode(mac.digest()).decode()
    
    def _req(self, method, path, body=None):
        ts = self._ts()
        msg = ts + method + path + (json.dumps(body) if body else '')
        headers = {
            'OK-ACCESS-KEY': API_KEY,
            'OK-ACCESS-SIGN': self._sign(msg),
            'OK-ACCESS-TIMESTAMP': ts,
            'OK-ACCESS-PASSPHRASE': PASSPHRASE,
            'Content-Type': 'application/json'
        }
        r = requests.request(method, BASE_URL + path, headers=headers, json=body)
        return r.json()
    
    def balance(self):
        return self._req('GET', '/api/v5/account/balance')
    
    def price(self, pair="BTC-USDT"):
        return self._req('GET', f'/api/v5/market/ticker?instId={pair}')
    
    def order(self, pair, side, sz, type="market", px=None):
        body = {"instId": pair, "tdMode": "cash", "side": side, "ordType": type, "sz": str(sz)}
        if px and type == "limit": body["px"] = str(px)
        return self._req('POST', '/api/v5/trade/order', body)
    
    def positions(self):
        return self._req('GET', '/api/v5/account/positions')
    
    def pending(self):
        return self._req('GET', '/api/v5/trade/orders-pending')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--action', choices=['balance','price','order','positions','pending'], default='balance')
    p.add_argument('--pair', default='BTC-USDT')
    p.add_argument('--side', choices=['buy','sell'])
    p.add_argument('--amount', type=float)
    p.add_argument('--type', choices=['market','limit'], default='market')
    p.add_argument('--price', type=float)
    args = p.parse_args()
    
    t = OKXTrader()
    
    if args.action == 'balance':
        r = t.balance()
        if r.get('code') == '0':
            print("=== Balance ===")
            for d in r['data'][0].get('details',[]):
                eq, usd = float(d['eq']), float(d['eqUsd'])
                if eq > 0: print(f"  {d['ccy']}: {eq:.8f} (${usd:.4f})")
            print(f"Total: ${float(r['data'][0]['totalEq']):.4f}")
        else: print("Error:", r)
    
    elif args.action == 'price':
        r = t.price(args.pair)
        if r.get('code') == '0':
            d = r['data'][0]
            print(f"=== {args.pair} ===")
            print(f"Last: ${float(d['last']):,.2f}")
            print(f"24h High: ${float(d['high24h']):,.2f}")
            print(f"24h Low: ${float(d['low24h']):,.2f}")
        else: print("Error:", r)
    
    elif args.action == 'order':
        if not args.side or not args.amount:
            print("Usage: --action order --side buy/sell --amount 0.001")
            return
        r = t.order(args.pair, args.side, args.amount, args.type, args.price)
        print("Order:", json.dumps(r, indent=2))
    
    elif args.action == 'positions':
        print(json.dumps(t.positions(), indent=2))
    
    elif args.action == 'pending':
        print(json.dumps(t.pending(), indent=2))

if __name__ == '__main__':
    main()
