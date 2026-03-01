#!/usr/bin/env python3
"""
股票分析脚本
依赖: yfinance, pandas, numpy
"""

import argparse
import sys
import subprocess
from datetime import datetime, timedelta


def ensure_deps():
    """确保依赖已安装"""
    try:
        import yfinance
        import pandas
        import numpy
    except ImportError:
        print("正在安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yfinance", "pandas", "numpy", "-q"], check=True)


def analyze_stock(symbol):
    """分析股票"""
    import yfinance as yf
    import pandas as pd
    import numpy as np
    
    # 转换股票代码格式
    # A股: 000001.SZ -> 000001.SS (上海) 或保持 .SZ (深圳)
    # 港股: 00700.HK -> 0700.HK
    
    print(f"正在获取 {symbol} 的数据...")
    
    stock = yf.Ticker(symbol)
    
    # 获取历史数据 (60天)
    hist = stock.history(period="60d")
    
    if hist.empty:
        print(f"❌ 无法获取 {symbol} 的数据")
        return
    
    # 基本信息
    info = stock.info
    name = info.get('longName', symbol)
    current_price = hist['Close'][-1]
    prev_price = hist['Close'][-2]
    change = (current_price - prev_price) / prev_price * 100
    
    print(f"\n{'='*50}")
    print(f"📊 {name} ({symbol})")
    print(f"{'='*50}")
    print(f"💰 当前价格: ${current_price:.2f} ({change:+.2f}%)")
    
    # 52周高低
    high_52w = hist['High'].max()
    low_52w = hist['Low'].min()
    print(f"📈 52周最高: ${high_52w:.2f}")
    print(f"📉 52周最低: ${low_52w:.2f}")
    
    # 移动平均线
    ma5 = hist['Close'].rolling(5).mean().iloc[-1]
    ma10 = hist['Close'].rolling(10).mean().iloc[-1]
    ma20 = hist['Close'].rolling(20).mean().iloc[-1]
    
    print(f"\n📊 技术指标")
    print(f"   MA5:  ${ma5:.2f}")
    print(f"   MA10: ${ma10:.2f}")
    print(f"   MA20: ${ma20:.2f}")
    
    # 趋势判断
    trend = ""
    if current_price > ma5 > ma10 > ma20:
        trend = "🟢 强势上涨"
    elif current_price > ma5 > ma10:
        trend = "🟡 短期上涨"
    elif current_price < ma5 < ma10 < ma20:
        trend = "🔴 下跌趋势"
    else:
        trend = "⚪ 震荡整理"
    
    print(f"\n📈 趋势判断: {trend}")
    
    # 成交量分析
    avg_volume = hist['Volume'].mean()
    latest_volume = hist['Volume'][-1]
    vol_ratio = latest_volume / avg_volume
    
    print(f"\n📦 成交量")
    print(f"   平均: {avg_volume:,.0f}")
    print(f"   最新: {latest_volume:,.0f} ({vol_ratio:.1f}x)")
    
    # 波动率
    volatility = hist['Close'].pct_change().std() * np.sqrt(252) * 100
    print(f"\n📊 波动率: {volatility:.1f}% (年化)")
    
    print(f"\n{'='*50}")
    print("⚠️  免责声明: 以上分析仅供参考，不构成投资建议")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="股票分析")
    parser.add_argument("symbol", help="股票代码 (如: 00700.HK, AAPL, 000001.SS)")
    
    args = parser.parse_args()
    
    ensure_deps()
    analyze_stock(args.symbol)


if __name__ == "__main__":
    main()
