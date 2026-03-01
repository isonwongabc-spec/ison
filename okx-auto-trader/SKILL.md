---
name: okx-auto-trader
description: OKX 桌面软件自动化工具。启动 OKX 并自动导航到指定交易对界面。当用户说"打开OKX BTC合约"或需要自动化操作 OKX 软件时使用。
---

# OKX Auto Trader

## 使用方式

```bash
# 打开 OKX 并导航到 BTC 合约
python {baseDir}/scripts/open_okx.py --pair BTC --type swap

# 打开 ETH 合约
python {baseDir}/scripts/open_okx.py --pair ETH --type swap

# 只启动软件
python {baseDir}/scripts/open_okx.py
```

## 支持的参数

- `--pair`: 交易对 (BTC, ETH, SOL 等)
- `--type`: 类型 (swap=合约, spot=现货)

## 自动化流程

1. 启动 OKX 桌面软件
2. 点击"交易"选项
3. 点击"合约"或"现货"
4. 搜索并选择指定币种
