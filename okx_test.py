import hmac
import hashlib
import base64
import json
from datetime import datetime, timezone
import requests

# API 配置
API_KEY = "112e3b78-387e-4df7-95ee-4f92f15d7d69"
API_SECRET = "4BF0777097F46740226B055B896D2CB1"
PASSPHRASE = "Abc32421."
BASE_URL = "https://www.okx.com"

def get_timestamp():
    # ISO 8601 格式
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def sign(message, secret):
    mac = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode('utf-8')

def make_request(method, path, body=None):
    timestamp = get_timestamp()
    message = timestamp + method + path + (json.dumps(body) if body else '')
    signature = sign(message, API_SECRET)
    
    headers = {
        'OK-ACCESS-KEY': API_KEY,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': PASSPHRASE,
        'Content-Type': 'application/json'
    }
    
    url = BASE_URL + path
    
    try:
        response = requests.request(method, url, headers=headers, json=body)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# 测试获取账户余额
result = make_request('GET', '/api/v5/account/balance')
print(json.dumps(result, indent=2, ensure_ascii=False))
