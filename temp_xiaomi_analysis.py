#!/usr/bin/env python3
"""小米股票分析"""
import yfinance as yf
import numpy as np

stock = yf.Ticker('1810.HK')
hist = stock.history(period='60d')
info = stock.info

name = info.get('longName', '1810.HK')
current = hist['Close'].iloc[-1]
prev = hist['Close'].iloc[-2]
change = (current - prev) / prev * 100

print("=" * 50)
print(f"📊 {name} (1810.HK)")
print("=" * 50)
print(f"💰 当前价格: HK${current:.2f} ({change:+.2f}%)")

# 60日高低
high_60d = hist['High'].max()
low_60d = hist['Low'].min()
print(f"📈 60日最高: HK${high_60d:.2f}")
print(f"📉 60日最低: HK${low_60d:.2f}")

# 移动平均线
ma5 = hist['Close'].rolling(5).mean().iloc[-1]
ma10 = hist['Close'].rolling(10).mean().iloc[-1]
ma20 = hist['Close'].rolling(20).mean().iloc[-1]

print(f"\n📊 技术指标")
print(f"   MA5:  HK${ma5:.2f}")
print(f"   MA10: HK${ma10:.2f}")
print(f"   MA20: HK${ma20:.2f}")

# 趋势判断
if current > ma5 > ma10 > ma20:
    trend = "🟢 强势上涨"
elif current > ma5 > ma10:
    trend = "🟡 短期上涨"
elif current < ma5 < ma10 < ma20:
    trend = "🔴 下跌趋势"
else:
    trend = "⚪ 震荡整理"

print(f"\n📈 趋势判断: {trend}")

# 位置分析
position = (current - low_60d) / (high_60d - low_60d) * 100
print(f"📍 当前位置: 60日区间的 {position:.1f}% 位置")

# 成交量
avg_vol = hist['Volume'].mean()
latest_vol = hist['Volume'].iloc[-1]
print(f"\n📦 成交量: {latest_vol:,.0f} (平均: {avg_vol:,.0f})")

# 波动率
volatility = hist['Close'].pct_change().std() * np.sqrt(252) * 100
print(f"📊 波动率: {volatility:.1f}% (年化)")

print("\n" + "=" * 50)
print("⚠️  免责声明: 以上分析仅供参考，不构成投资建议")
print("=" * 50)