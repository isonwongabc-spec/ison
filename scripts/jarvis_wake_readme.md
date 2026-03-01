# Jarvis 语音唤醒系统 - 快速启动指南

## 🎙️ 方案选择

### 方案1：Porcupine（推荐）- 需要注册
- 准确率高，支持 "Jarvis" 唤醒词
- 本地运行，无需联网
- 免费个人使用

**注册步骤：**
1. 访问 https://picovoice.ai/
2. 注册免费账号
3. 复制 Access Key
4. 粘贴到下方配置文件

### 方案2：快捷键触发（临时）
- 按 `Ctrl+Alt+J` 触发 Jarvis
- 无需注册，立即使用

---

## ⚙️ 配置

### Porcupine 配置
编辑 `jarvis_config.txt`：
```
ACCESS_KEY=你的_picovoice_access_key
WAKE_WORD=jarvis
SENSITIVITY=0.8
```

### 快捷键配置
默认：`Ctrl+Alt+J`

---

## 🚀 启动唤醒

### 方法1：Porcupine 语音唤醒
```bash
python jarvis_wake_porcupine.py
```

### 方法2：快捷键触发
```bash
python jarvis_hotkey.py
```

---

## 📝 唤醒后操作

唤醒后可以执行：
- 语音指令输入
- 打开指定软件
- 执行系统命令
- 发送通知

---

## 🔧 故障排除

**问题：麦克风无法识别**
- 检查麦克风权限
- 设置默认录音设备

**问题：唤醒不灵敏**
- 调整 SENSITIVITY（0.5-1.0）
- 靠近麦克风说话

---

**现在选择方案：**
回复 "1" 使用 Porcupine（需要去网站注册）
回复 "2" 使用快捷键（立即使用）
