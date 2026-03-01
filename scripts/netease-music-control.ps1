# 网易云音乐 (YesPlayMusic) 控制脚本
# 用于控制 YesPlayMusic 播放器

param(
    [Parameter()]
    [ValidateSet("play", "pause", "toggle", "next", "prev", "search", "volume-up", "volume-down", "mute", "status", "launch")]
    [string]$Action = "status",
    
    [string]$Query = ""
)

$appName = "YesPlayMusic"
$exePath = "$env:LOCALAPPDATA\Programs\yesplaymusic\YesPlayMusic.exe"

function Get-YesPlayMusicProcess {
    return Get-Process | Where-Object { $_.ProcessName -like "*YesPlayMusic*" -and $_.ProcessName -ne "YesPlayMusic-Installer" } | Select-Object -First 1
}

function Launch-YesPlayMusic {
    if (Test-Path $exePath) {
        Start-Process $exePath
        Write-Host "✅ YesPlayMusic 已启动"
        Start-Sleep -Seconds 3
    } else {
        Write-Host "❌ 未找到 YesPlayMusic，请确认已安装"
        exit 1
    }
}

function Send-MediaKey {
    param([string]$key)
    
    $wsh = New-Object -ComObject WScript.Shell
    $proc = Get-YesPlayMusicProcess
    
    if ($proc) {
        $wsh.AppActivate($proc.Id)
        Start-Sleep -Milliseconds 200
        
        switch ($key) {
            "play-pause" { $wsh.SendKeys("{MEDIA_PLAY_PAUSE}") }
            "next" { $wsh.SendKeys("{MEDIA_NEXT}") }
            "prev" { $wsh.SendKeys("{MEDIA_PREV}") }
            "volume-up" { 
                for ($i = 0; $i -lt 5; $i++) { $wsh.SendKeys("{VOLUME_UP}") }
            }
            "volume-down" { 
                for ($i = 0; $i -lt 5; $i++) { $wsh.SendKeys("{VOLUME_DOWN}") }
            }
            "mute" { $wsh.SendKeys("{VOLUME_MUTE}") }
        }
        return $true
    }
    return $false
}

function Search-Music {
    param([string]$keyword)
    
    $wsh = New-Object -ComObject WScript.Shell
    $proc = Get-YesPlayMusicProcess
    
    if (-not $proc) {
        Launch-YesPlayMusic
        $proc = Get-YesPlayMusicProcess
    }
    
    if ($proc) {
        $wsh.AppActivate($proc.Id)
        Start-Sleep -Milliseconds 500
        
        # Ctrl+F 打开搜索
        $wsh.SendKeys("^f")
        Start-Sleep -Milliseconds 300
        
        # 输入搜索关键词
        $wsh.SendKeys("^a")
        Start-Sleep -Milliseconds 100
        $wsh.SendKeys($keyword)
        Start-Sleep -Milliseconds 300
        $wsh.SendKeys("{ENTER}")
        
        Write-Host "✅ 已搜索: $keyword"
        Write-Host "💡 请在 YesPlayMusic 窗口中点击歌曲播放"
    }
}

# 主逻辑
switch ($Action) {
    "launch" { Launch-YesPlayMusic }
    "play" { 
        if (Send-MediaKey "play-pause") { Write-Host "▶️ 播放" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "pause" { 
        if (Send-MediaKey "play-pause") { Write-Host "⏸️ 暂停" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "toggle" { 
        if (Send-MediaKey "play-pause") { Write-Host "⏯️ 播放/暂停切换" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "next" { 
        if (Send-MediaKey "next") { Write-Host "⏭️ 下一首" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "prev" { 
        if (Send-MediaKey "prev") { Write-Host "⏮️ 上一首" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "volume-up" { 
        if (Send-MediaKey "volume-up") { Write-Host "🔊 音量增加" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "volume-down" { 
        if (Send-MediaKey "volume-down") { Write-Host "🔉 音量减小" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "mute" { 
        if (Send-MediaKey "mute") { Write-Host "🔇 静音" }
        else { Write-Host "❌ YesPlayMusic 未运行" }
    }
    "search" { 
        if ($Query) { Search-Music $Query }
        else { Write-Host "❌ 请提供搜索关键词，如: -Query '卫蘭'" }
    }
    "status" {
        $proc = Get-YesPlayMusicProcess
        if ($proc) {
            Write-Host "✅ YesPlayMusic 正在运行 (PID: $($proc.Id))"
        } else {
            Write-Host "ℹ️ YesPlayMusic 未运行"
            Write-Host "💡 使用 -Action launch 启动"
        }
    }
}
