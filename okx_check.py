import requests
import json

# OKX 公开 API - 不需要认证
BASE_URL = "https://www.okx.com"

# 测试几个公开端点
endpoints = [
    "/api/v5/market/tickers?instType=SPOT",
    "/api/v5/public/instruments?instType=SPOT",
]

for path in endpoints:
    try:
        r = requests.get(BASE_URL + path, timeout=10)
        print(f"\n=== {path} ===")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Data keys: {data.keys()}")
    except Exception as e:
        print(f"Error: {e}")

# 检查是否有新闻/公告 API
try:
    r = requests.get("https://www.okx.com/api/v5/public/announcements", timeout=10)
    print(f"\n=== Announcements ===")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(r.text[:500])
except Exception as e:
    print(f"Announcements endpoint error: {e}")
