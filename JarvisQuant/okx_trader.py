import requests
import hmac
import hashlib
import base64
import json
from datetime import datetime, timezone

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
        request_path = '/api/v5/account/balance'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def get_positions(self):
        request_path = '/api/v5/account/positions'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def get_ticker(self, symbol):
        request_path = f'/api/v5/market/ticker?instId={symbol}'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def place_order(self, symbol, side, pos_side, sz, ord_type='market', px=None):
        body = {
            'instId': symbol,
            'tdMode': 'cross',
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
        body = {
            'instId': symbol,
            'mgnMode': 'cross',
            'posSide': 'long'
        }
        body_json = json.dumps(body)
        request_path = '/api/v5/trade/close-position'
        headers = self._get_headers('POST', request_path, body_json)
        response = requests.post(self.base_url + request_path, headers=headers, data=body_json)
        return response.json()
    
    def get_funding_balance(self):
        request_path = '/api/v5/asset/balances'
        headers = self._get_headers('GET', request_path)
        response = requests.get(self.base_url + request_path, headers=headers)
        return response.json()
    
    def transfer_to_trading(self, ccy, amt):
        body = {
            'ccy': ccy,
            'amt': str(amt),
            'from': '6',
            'to': '18'
        }
        body_json = json.dumps(body)
        request_path = '/api/v5/asset/transfer'
        headers = self._get_headers('POST', request_path, body_json)
        response = requests.post(self.base_url + request_path, headers=headers, data=body_json)
        return response.json()
