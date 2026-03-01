# OpenClaw Windows 自动安装脚本
# 以管理员身份运行 PowerShell，然后执行此脚本

Write-Host "=== OpenClaw Windows 安装脚本 ===" -ForegroundColor Green

# 检查管理员权限
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "请以管理员身份运行此脚本！" -ForegroundColor Red
    exit
}

# 1. 检查 Node.js
Write-Host "\n[1/5] 检查 Node.js..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "Node.js 未安装，请先安装: https://nodejs.org/" -ForegroundColor Red
    exit
}
Write-Host "Node.js 版本: $(node --version)" -ForegroundColor Green

# 2. 检查 Python
Write-Host "\n[2/5] 检查 Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python 未安装，请先安装: https://www.python.org/downloads/" -ForegroundColor Red
    exit
}
Write-Host "Python 版本: $(python --version)" -ForegroundColor Green

# 3. 检查 Git
Write-Host "\n[3/5] 检查 Git..." -ForegroundColor Yellow
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Host "Git 未安装，请先安装: https://git-scm.com/download/win" -ForegroundColor Red
    exit
}
Write-Host "Git 版本: $(git --version)" -ForegroundColor Green

# 4. 安装 OpenClaw
Write-Host "\n[4/5] 安装 OpenClaw..." -ForegroundColor Yellow
npm install -g openclaw-cn
if ($LASTEXITCODE -ne 0) {
    Write-Host "OpenClaw 安装失败！" -ForegroundColor Red
    exit
}
Write-Host "OpenClaw 安装成功！" -ForegroundColor Green

# 5. 克隆仓库
Write-Host "\n[5/5] 克隆你的配置仓库..." -ForegroundColor Yellow
$repoUrl = Read-Host "请输入你的 GitHub 仓库地址 (如: https://github.com/username/repo.git)"
$targetDir = "$env:USERPROFILE\.openclaw"

if (Test-Path $targetDir) {
    Write-Host "目录已存在，正在更新..." -ForegroundColor Yellow
    Set-Location $targetDir
    git pull
} else {
    Write-Host "正在克隆仓库到 $targetDir..." -ForegroundColor Yellow
    git clone $repoUrl $targetDir
}

Write-Host "\n=== 安装完成！ ===" -ForegroundColor Green
Write-Host "\n下一步:" -ForegroundColor Cyan
Write-Host "1. 运行 'openclaw-cn gateway init' 初始化配置" -ForegroundColor White
Write-Host "2. 运行 'openclaw-cn configure --section telegram' 配置 Telegram" -ForegroundColor White
Write-Host "3. 运行 'openclaw-cn gateway start' 启动服务" -ForegroundColor White
Write-Host "\n你的脚本和配置文件已同步到: $targetDir" -ForegroundColor Green