# 社交媒体监控系统配置脚本
# 用于配置小红书 + 抖音双平台监控

param(
    [Parameter()]
    [ValidateSet("setup", "run", "status")]
    [string]$Action = "status",
    
    [string[]]$XhsTopics = @(),
    [string[]]$DouyinAccounts = @(),
    [string]$Schedule = "0 */6 * * *"
)

$configPath = "$env:USERPROFILE\.openclaw\workspace\memory\social-monitor-config.json"
$logPath = "$env:USERPROFILE\.openclaw\workspace\memory\social-monitor.log"

function Load-Config {
    if (Test-Path $configPath) {
        return Get-Content $configPath | ConvertFrom-Json
    }
    return @{
        status = "not_configured"
        xiaohongshu = @{ enabled = $false; topics = @(); accounts = @(); schedule = "0 */6 * * *" }
        douyin = @{ enabled = $false; accounts = @(); topics = @(); schedule = "0 */6 * * *" }
    }
}

function Save-Config($config) {
    $config | ConvertTo-Json -Depth 10 | Out-File $configPath -Encoding UTF8
}

function Setup-Monitor {
    Write-Host "🚀 配置社交媒体监控系统" -ForegroundColor Cyan
    Write-Host ""
    
    $config = Load-Config
    
    # 配置小红书
    Write-Host "📕 小红书配置" -ForegroundColor Yellow
    $enableXhs = Read-Host "是否启用小红书监控? (y/n)"
    if ($enableXhs -eq "y" -or $enableXhs -eq "Y") {
        $config.xiaohongshu.enabled = $true
        $topics = Read-Host "输入要监控的话题/关键词（用逗号分隔）"
        $config.xiaohongshu.topics = $topics -split "," | ForEach-Object { $_.Trim() }
        Write-Host "✅ 小红书监控已启用，监控话题: $($config.xiaohongshu.topics -join ', ')" -ForegroundColor Green
    }
    
    # 配置抖音
    Write-Host ""
    Write-Host "🎵 抖音配置" -ForegroundColor Yellow
    $enableDouyin = Read-Host "是否启用抖音监控? (y/n)"
    if ($enableDouyin -eq "y" -or $enableDouyin -eq "Y") {
        $config.douyin.enabled = $true
        $accounts = Read-Host "输入要监控的抖音账号（用逗号分隔，可选）"
        if ($accounts) {
            $config.douyin.accounts = $accounts -split "," | ForEach-Object { $_.Trim() }
        }
        Write-Host "✅ 抖音监控已启用" -ForegroundColor Green
    }
    
    # 配置频率
    Write-Host ""
    Write-Host "⏰ 监控频率" -ForegroundColor Yellow
    Write-Host "1) 每6小时 (默认)"
    Write-Host "2) 每12小时"
    Write-Host "3) 每天一次"
    Write-Host "4) 每小时"
    $freq = Read-Host "选择频率 (1-4)"
    switch ($freq) {
        "2" { $config.xiaohongshu.schedule = "0 */12 * * *"; $config.douyin.schedule = "0 */12 * * *" }
        "3" { $config.xiaohongshu.schedule = "0 9 * * *"; $config.douyin.schedule = "0 9 * * *" }
        "4" { $config.xiaohongshu.schedule = "0 * * * *"; $config.douyin.schedule = "0 * * * *" }
        default { $config.xiaohongshu.schedule = "0 */6 * * *"; $config.douyin.schedule = "0 */6 * * *" }
    }
    
    $config.status = "configured"
    Save-Config $config
    
    Write-Host ""
    Write-Host "✅ 监控配置完成！" -ForegroundColor Green
    Show-Status
}

function Run-Monitor {
    $config = Load-Config
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Add-Content -Path $logPath -Value "[$timestamp] 开始监控任务..."
    
    # 小红书监控
    if ($config.xiaohongshu.enabled) {
        Write-Host "📕 正在监控小红书..." -ForegroundColor Yellow
        foreach ($topic in $config.xiaohongshu.topics) {
            Write-Host "  搜索话题: $topic"
            # 这里调用小红书API
            Add-Content -Path $logPath -Value "[$timestamp] 小红书 - 搜索: $topic"
        }
    }
    
    # 抖音监控
    if ($config.douyin.enabled) {
        Write-Host "🎵 正在监控抖音..." -ForegroundColor Yellow
        Add-Content -Path $logPath -Value "[$timestamp] 抖音 - 监控账号"
    }
    
    $config.last_run = $timestamp
    Save-Config $config
    
    Add-Content -Path $logPath -Value "[$timestamp] 监控任务完成"
}

function Show-Status {
    $config = Load-Config
    
    Write-Host ""
    Write-Host "📊 社交媒体监控状态" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Gray
    
    Write-Host "状态: $($config.status)" -ForegroundColor $(if ($config.status -eq "configured") { "Green" } else { "Red" })
    
    Write-Host ""
    Write-Host "📕 小红书" -ForegroundColor Yellow
    Write-Host "  启用: $($config.xiaohongshu.enabled)"
    if ($config.xiaohongshu.enabled) {
        Write-Host "  监控话题: $($config.xiaohongshu.topics -join ', ')"
        Write-Host "  执行频率: $($config.xiaohongshu.schedule)"
    }
    
    Write-Host ""
    Write-Host "🎵 抖音" -ForegroundColor Yellow
    Write-Host "  启用: $($config.douyin.enabled)"
    if ($config.douyin.enabled) {
        if ($config.douyin.accounts.Count -gt 0) {
            Write-Host "  监控账号: $($config.douyin.accounts -join ', ')"
        }
        Write-Host "  执行频率: $($config.douyin.schedule)"
    }
    
    if ($config.last_run) {
        Write-Host ""
        Write-Host "⏰ 上次运行: $($config.last_run)"
    }
    
    Write-Host ""
    Write-Host "================================" -ForegroundColor Gray
}

# 主逻辑
switch ($Action) {
    "setup" { Setup-Monitor }
    "run" { Run-Monitor }
    "status" { Show-Status }
}
