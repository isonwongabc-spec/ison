"""
Multi-Exchange Trading Interface
Abstract base class and implementations for various exchanges
"""

from abc import ABC, abstractmethod
import requests
import hmac
import hashlib
import base64
import json
from datetime import datetime, timezone

class ExchangeInterface(ABC):
    """Abstract base class for exchange interfaces"""
    
    def __init__(self, api_key, api_secret, passphrase=None, testnet=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.testnet = testnet
        
    @abstractmethod
    def get_balance(self):
        """Get account balance"""
        pass
    
    @abstractmethod
    def get_positions(self):
        """Get current positions"""
        pass
    
    @abstractmethod
    def get_ticker(self, symbol):
        """Get current price ticker"""
        pass
    
    @abstractmethod
    def place_order(self, symbol, side, pos_side, sz, ord_type='market', px=None):
        """Place an order"""
        pass
    
    @abstractmethod
    def close_position(self, symbol):
        """Close position"""
        pass
    
    @abstractmethod
    def get_symbol_format(self, base, quote, contract=True):
        """Convert base-quote to exchange-specific symbol format"""
        pass


class OKXExchange(ExchangeInterface):
    """OKX Exchange Implementation"""
    
    def __init__(self, api_key, api_secret, passphrase, testnet=False):
        super().__init__(api_key, api_secret, passphrase, testnet)
        self.base_url = "https://www.okx.com"
        if testnet:
            self.base_url = "https://www.okx.com"  # OKX testnet URL
    
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
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': sign,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        return headers
    
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
    
    def get_symbol_format(self, base, quote, contract=True):
        """Convert to OKX format: ETH-USDT-SWAP"""
        if contract:
            return f"{base}-{quote}-SWAP"
        return f"{base}-{quote}"


class BinanceExchange(ExchangeInterface):
    """Binance Exchange Implementation"""
    
    def __init__(self, api_key, api_secret, passphrase=None, testnet=False):
        super().__init__(api_key, api_secret, passphrase, testnet)
        self.base_url = "https://fapi.binance.com"  # Futures API
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
    
    def _get_timestamp(self):
        return str(int(datetime.now(timezone.utc).timestamp() * 1000))
    
    def _sign(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self):
        return {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def get_balance(self):
        timestamp = self._get_timestamp()
        query = f"timestamp={timestamp}"
        signature = self._sign(query)
        url = f"{self.base_url}/fapi/v2/balance?{query}&signature={signature}"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    def get_positions(self):
        timestamp = self._get_timestamp()
        query = f"timestamp={timestamp}"
        signature = self._sign(query)
        url = f"{self.base_url}/fapi/v2/positionRisk?{query}&signature={signature}"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    def get_ticker(self, symbol):
        url = f"{self.base_url}/fapi/v1/ticker/price?symbol={symbol}"
        response = requests.get(url)
        return response.json()
    
    def place_order(self, symbol, side, pos_side, sz, ord_type='MARKET', px=None):
        timestamp = self._get_timestamp()
        
        # Binance uses BUY/SELL for side
        binance_side = side.upper()
        
        params = {
            'symbol': symbol,
            'side': binance_side,
            'type': ord_type.upper(),
            'quantity': sz,
            'timestamp': timestamp
        }
        
        if ord_type.upper() == 'LIMIT' and px:
            params['price'] = px
            params['timeInForce'] = 'GTC'
        
        query = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = self._sign(query)
        url = f"{self.base_url}/fapi/v1/order?{query}&signature={signature}"
        
        response = requests.post(url, headers=self._get_headers())
        return response.json()
    
    def close_position(self, symbol):
        # Binance closes by placing opposite order
        return self.place_order(symbol, 'SELL', 'short', 0)  # Size should be actual position size
    
    def get_symbol_format(self, base, quote, contract=True):
        """Convert to Binance format: ETHUSDT"""
        return f"{base}{quote}"


class BybitExchange(ExchangeInterface):
    """Bybit Exchange Implementation"""
    
    def __init__(self, api_key, api_secret, passphrase=None, testnet=False):
        super().__init__(api_key, api_secret, passphrase, testnet)
        self.base_url = "https://api.bybit.com"
        if testnet:
            self.base_url = "https://api-testnet.bybit.com"
    
    def _get_timestamp(self):
        return str(int(datetime.now(timezone.utc).timestamp() * 1000))
    
    def _sign(self, payload):
        timestamp = self._get_timestamp()
        param_str = timestamp + self.api_key + '5000' + payload
        hash = hmac.new(
            self.api_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return timestamp, hash
    
    def _get_headers(self, payload='{}'):
        timestamp, sign = self._sign(payload)
        return {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': sign,
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': '5000',
            'Content-Type': 'application/json'
        }
    
    def get_balance(self):
        payload = '{}'
        url = f"{self.base_url}/v5/account/wallet-balance?accountType=UNIFIED"
        response = requests.get(url, headers=self._get_headers(payload))
        return response.json()
    
    def get_positions(self):
        payload = '{}'
        url = f"{self.base_url}/v5/position/list?category=linear&symbol=ETHUSDT"
        response = requests.get(url, headers=self._get_headers(payload))
        return response.json()
    
    def get_ticker(self, symbol):
        url = f"{self.base_url}/v5/market/tickers?category=linear&symbol={symbol}"
        response = requests.get(url)
        return response.json()
    
    def place_order(self, symbol, side, pos_side, sz, ord_type='Market', px=None):
        body = {
            'category': 'linear',
            'symbol': symbol,
            'side': side.capitalize(),
            'orderType': ord_type.capitalize(),
            'qty': str(sz)
        }
        if px and ord_type.lower() == 'limit':
            body['price'] = str(px)
        
        payload = json.dumps(body)
        url = f"{self.base_url}/v5/order/create"
        response = requests.post(url, headers=self._get_headers(payload), data=payload)
        return response.json()
    
    def close_position(self, symbol):
        # Bybit closes via position endpoint
        payload = json.dumps({
            'category': 'linear',
            'symbol': symbol
        })
        url = f"{self.base_url}/v5/position/close-pnl"
        response = requests.post(url, headers=self._get_headers(payload), data=payload)
        return response.json()
    
    def get_symbol_format(self, base, quote, contract=True):
        """Convert to Bybit format: ETHUSDT"""
        return f"{base}{quote}"


class ExchangeFactory:
    """Factory for creating exchange instances"""
    
    @staticmethod
    def create_exchange(exchange_name, api_key, api_secret, passphrase=None, testnet=False):
        """Create exchange instance by name"""
        exchanges = {
            'okx': OKXExchange,
            'binance': BinanceExchange,
            'bybit': BybitExchange
        }
        
        exchange_class = exchanges.get(exchange_name.lower())
        if not exchange_class:
            raise ValueError(f"Unsupported exchange: {exchange_name}")
        
        return exchange_class(api_key, api_secret, passphrase, testnet)
    
    @staticmethod
    def get_supported_exchanges():
        """Get list of supported exchanges"""
        return ['okx', 'binance', 'bybit']


if __name__ == '__main__':
    # Test OKX connection - REPLACE WITH YOUR OWN API KEYS
    print("Testing OKX Exchange...")
    okx = ExchangeFactory.create_exchange(
        'okx',
        'YOUR_API_KEY',
        'YOUR_API_SECRET',
        'YOUR_PASSPHRASE'
    )
    
    balance = okx.get_balance()
    print(f"OKX Balance: {balance.get('code') == '0' and 'Connected' or 'Failed'}")
    
    # Test symbol formatting
    print(f"\nSymbol Format Examples:")
    print(f"OKX ETH/USDT: {okx.get_symbol_format('ETH', 'USDT')}")
    
    binance = ExchangeFactory.create_exchange('binance', 'test', 'test')
    print(f"Binance ETH/USDT: {binance.get_symbol_format('ETH', 'USDT')}")
    
    bybit = ExchangeFactory.create_exchange('bybit', 'test', 'test')
    print(f"Bybit ETH/USDT: {bybit.get_symbol_format('ETH', 'USDT')}")
