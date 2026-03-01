---
name: video-downloader
description: 下载 B站/YouTube 视频并生成分享链接。当用户说"下载这个视频"、"帮我下载 B站/YouTube 视频"或提供视频链接时使用。
---

# Video Downloader

## 使用方式

```bash
# 下载 YouTube 视频
python {baseDir}/scripts/download.py "https://youtube.com/watch?v=xxxxx"

# 下载 B站视频
python {baseDir}/scripts/download.py "https://bilibili.com/video/BVxxxxx"

# 指定格式（可选）
python {baseDir}/scripts/download.py "URL" --format mp4
```

## 支持的网站

- YouTube
- Bilibili (B站)
- 以及其他 yt-dlp 支持的网站

## 输出

- 下载的视频文件保存在 `downloads/` 目录
- 生成分享链接（可配置）
