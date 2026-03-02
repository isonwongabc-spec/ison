import requests
import hmac
import hashlib
import base64
import json
from datetime import datetime, timezone
import time

class OKXTrader:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = "https://www.okx.com"
        self.simulated = False  # LIVE TRADING MODE
    
    def _get_timestamp(self):
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def _sign(self, timestamp, method, request_path, body=''):
        message = timestamp + method.upper() + request_path + body
        mac = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode('utf-8')
    
    def _get_headers(self, method, request_path, body=''):
        timestamp = self._get_timestamp()
        sign = self._sign(timestamp, method, request_path, body)
        return {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': sign,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
    
    def get_balance(self):
        """Get account balance"""
        request_path = '/api/v5/account/balance'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def get_positions(self):
        """Get current positions"""
        request_path = '/api/v5/account/positions'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def get_ticker(self, symbol):
        """Get current price"""
        request_path = f'/api/v5/market/ticker?instId={symbol}'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def place_order(self, symbol, side, pos_side, sz, ord_type='market', px=None):
        """Place an order"""
        if self.simulated:
            print(f"[SIMULATED] {side} {pos_side} {sz} {symbol}")
            return {'simulated': True, 'symbol': symbol, 'side': side, 'size': sz}
        
        body = {
            'instId': symbol,
            'tdMode': 'cross',  # Cross margin
            'side': side,
            'posSide': pos_side,
            'ordType': ord_type,
            'sz': str(sz)
        }
        if px:
            body['px'] = str(px)
        
        body_json = json.dumps(body)
        request_path = '/api/v5/trade/order'
        headers = self._get_headers('POST', request_path, body_json)
        response = requests.post(self.base_url + request_path, headers=headers, data=body_json)
        return response.json()
    
    def close_position(self, symbol):
        """Close position"""
        body = {
            'instId': symbol,
            'mgnMode': 'cross',
            'posSide': 'long'  # or 'short'
        }
        body_json = json.dumps(body)
        request_path = '/api/v5/trade/close-position'
        headers = self._get_headers('POST', request_path, body_json)
        response = requests.post(self.base_url + request_path, headers=headers, data=body_json)
        return response.json()
    
    def get_funding_balance(self):
        """Get funding account balance"""
        request_path = '/api/v5/asset/balances'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def transfer_to_trading(self, ccy, amt):
        """Transfer from funding to trading account"""
        body = {
            'ccy': ccy,
            'amt': str(amt),
            'from': '6',  # Funding account
            'to': '18'    # Trading account (Unified)
        }
        body_json = json.dumps(body)
        request_path = '/api/v5/asset/transfer'
        headers = self._get_headers('POST', request_path, body_json)
        response = requests.post(self.base_url + request_path, headers=headers, data=body_json)
        return response.json()

if __name__ == '__main__':
    # Test connection
    trader = OKXTrader(
        api_key='112e3b78-387e-4df7-95ee-4f92f15d7d69',
        api_secret='4BF0777097F46740226B055B896D2CB1',
        passphrase='Abc32421.'
    )
    
    print("Testing OKX API connection...")
    print("=" * 50)
    
    # Get balance
    balance = trader.get_balance()
    print("\nAccount Balance:")
    print(json.dumps(balance, indent=2))
    
    # Get ETH price
    eth_price = trader.get_ticker('ETH-USDT-SWAP')
    print("\nETH Price:")
    print(json.dumps(eth_price, indent=2))
    
    # Get BTC price
    btc_price = trader.get_ticker('BTC-USDT-SWAP')
    print("\nBTC Price:")
    print(json.dumps(btc_price, indent=2))
