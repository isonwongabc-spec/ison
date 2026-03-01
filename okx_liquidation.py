import requests
import json
from datetime import datetime

# OKX 爆仓数据（公开 API）
BASE_URL = "https://www.okx.com"

def get_okx_liquidations(inst_type="SWAP", limit=100):
    """获取 OKX 爆仓订单数据"""
    try:
        url = f"{BASE_URL}/api/v5/trade/fills-history?instType={inst_type}&limit={limit}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"error": f"Status {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_okx_mark_price(coin="BTC"):
    """获取标记价格"""
    try:
        url = f"{BASE_URL}/api/v5/market/mark-price?instType=SWAP&instId={coin}-USDT-SWAP"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return {"error": f"Status {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=== OKX 爆仓数据 ===\n")
    
    # 获取爆仓数据
    liq = get_okx_liquidations()
    if "error" not in liq and liq.get("code") == "0":
        print(f"获取到 {len(liq.get('data', []))} 条成交记录")
        print("\n样本数据:")
        for item in liq.get("data", [])[:3]:
            print(f"  {item.get('instId')}: {item.get('side')} {item.get('sz')} @ {item.get('fillPx')}")
    else:
        print("爆仓数据:", liq.get("error") or liq.get("msg"))
    
    print("\n=== BTC 标记价格 ===")
    mp = get_okx_mark_price("BTC")
    if "error" not in mp and mp.get("code") == "0":
        data = mp["data"][0]
        print(f"BTC 标记价格: ${float(data['markPx']):,.2f}")
    else:
        print("错误:", mp)
