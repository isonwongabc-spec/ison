import requests
import json
from datetime import datetime

# CoinGlass 公开数据抓取
BASE_URL = "https://www.coinglass.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

# 尝试获取爆仓数据
def get_liquidation_data():
    """获取爆仓数据"""
    try:
        # CoinGlass liquidation endpoint
        url = f"{BASE_URL}/api/liquidation/v3?timeType=1&size=50"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"error": f"Status {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 获取资金费率
def get_funding_rate():
    """获取资金费率数据"""
    try:
        url = f"{BASE_URL}/api/fundingRate/v3?size=50"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"error": f"Status {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 获取多空比
def get_long_short_ratio():
    """获取多空比数据"""
    try:
        url = f"{BASE_URL}/api/globalLongShortAccountRatio/v3?size=50"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"error": f"Status {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 获取持仓量
def get_open_interest():
    """获取持仓量数据"""
    try:
        url = f"{BASE_URL}/api/openInterest/v3?size=50"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"error": f"Status {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=== Testing CoinGlass Public Data ===\n")
    
    print("1. Liquidation Data:")
    liq = get_liquidation_data()
    print(json.dumps(liq, indent=2)[:500] if "error" not in liq else liq)
    
    print("\n2. Funding Rate:")
    fund = get_funding_rate()
    print(json.dumps(fund, indent=2)[:500] if "error" not in fund else fund)
    
    print("\n3. Long/Short Ratio:")
    lsr = get_long_short_ratio()
    print(json.dumps(lsr, indent=2)[:500] if "error" not in lsr else lsr)
    
    print("\n4. Open Interest:")
    oi = get_open_interest()
    print(json.dumps(oi, indent=2)[:500] if "error" not in oi else oi)
