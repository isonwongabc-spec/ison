# OpenClaw Windows 安装指南

## 1. 安装依赖

### 安装 Node.js
- 下载: https://nodejs.org/ (推荐 LTS 版本)
- 安装时勾选 "Add to PATH"

### 安装 Python
- 下载: https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

### 安装 Git
- 下载: https://git-scm.com/download/win

## 2. 安装 OpenClaw

打开 PowerShell 或 CMD，运行:

```bash
npm install -g openclaw-cn
```

## 3. 配置 Gateway

```bash
# 初始化配置
openclaw-cn gateway init

# 配置 Telegram (需要 Bot Token)
openclaw-cn configure --section telegram
```

## 4. 克隆你的仓库

```bash
cd C:\Users\你的用户名
git clone https://github.com/isonwongabc-spec/ison.git .openclaw
```

## 5. 启动 Gateway

```bash
openclaw-cn gateway start
```

## 6. 获取 Bot Token

1. 打开 Telegram，搜索 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 设置名称和用户名
4. 保存提供的 Token

## 7. 配置完成

用 Telegram 搜索你的机器人用户名，开始对话即可。

---

## 快速脚本

运行 `install_opencode.ps1` 自动安装（需管理员权限）:

```powershell
# 右键 PowerShell，选择"以管理员身份运行"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_opencode.ps1
```