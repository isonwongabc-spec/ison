# Infra - 基础设施速查

_服务器、API、配置信息。快速查找，不用翻聊天记录。_

## 本地环境

| 项目 | 路径/地址 | 备注 |
|------|----------|------|
| 工作目录 | C:\Users\USER\.openclaw\workspace | 所有文件在这里 |
| 微信 | D:\Weixin\Weixin.exe | 已配置自动启动 |
| Word | C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE | 已配置 |
| OKX 桌面软件 | D:\okx\OKX.exe | 已配置自动化 |
| OKX 网页版 | https://www.okx.com/trade-swap/btc-usdt-swap | 已配置 |
| 酷狗音乐 | C:\Program Files (x86)\KuGou\KGMusic\KuGou.exe | 已配置 |
| 网易云音乐 (YesPlayMusic) | %LOCALAPPDATA%\Programs\yesplaymusic\YesPlayMusic.exe | 已配置API控制 |
| 浏览器控制 (Playwright) | workspace/scripts/browser-control.js | ✅ 已修复，可点击、填表、截图 |

### OKX 自动化坐标 (1920x1080)
| 元素 | X | Y |
|------|---|---|
| 交易菜单 | 330 | 55 |
| 合约按钮 | 130 | 250 |
| 现货按钮 | 90 | 250 |
| BTCUSDT | 80 | 350 |
| ETHUSDT | 80 | 420 |
| Excel | C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE | 推测路径 |
| PowerPoint | C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE | 推测路径 |

## API Keys（待配置）

| 服务 | 状态 | 用途 |
|------|------|------|
| OKX API | ❌ 未配置 | 自动交易 |
| Gemini API | ❌ 未配置 | 图像生成 |
| OpenAI API | ❌ 未配置 | 图像/GPT |
| Brave Search | ❌ 未配置 | 网页搜索 |
| Tavily | ❌ 未配置 | AI 搜索 (刚安装) |

## 配置文件位置

| 文件 | 路径 |
|------|------|
| 自动启动软件配置 | auto-launch-apps.md |
| 身份档案 | IDENTITY.md |
| 灵魂档案 | SOUL.md |
| Boss 档案 | USER.md |
| 核心记忆 | MEMORY.md |

## 配置状态

| 配置项 | 状态 | 说明 |
|--------|------|------|
| compaction.memoryFlush | ✅ 已开启 | 上下文快满时自动把重要信息写入当天日志，防止"失忆" |

---

_Last updated: 2026-02-27_
