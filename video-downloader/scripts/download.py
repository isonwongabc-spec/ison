#!/usr/bin/env python3
"""
视频下载脚本 - 支持 YouTube、B站等
依赖: yt-dlp, requests
"""

import argparse
import os
import sys
from pathlib import Path
import subprocess
import json


def ensure_yt_dlp():
    """确保 yt-dlp 已安装"""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("正在安装 yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp", "-q"], check=True)


def download_video(url, output_dir="downloads", format_type="mp4"):
    """下载视频"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 配置 yt-dlp 选项
    ydl_opts = [
        "yt-dlp",
        "-f", f"bestvideo[ext={format_type}]+bestaudio[ext=m4a]/best[ext={format_type}]/best",
        "-o", f"{output_path}/%(title)s.%(ext)s",
        "--merge-output-format", format_type,
        "--no-warnings",
        "--progress",
        "-v",  # 显示视频信息
        url
    ]
    
    try:
        result = subprocess.run(ydl_opts, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 下载完成!")
            # 解析输出找到文件名
            for line in result.stderr.split('\n'):
                if '[download] Destination:' in line:
                    filepath = line.split('[download] Destination: ')[-1].strip()
                    print(f"📁 文件保存: {filepath}")
                    return filepath
        else:
            print(f"❌ 下载失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="下载视频")
    parser.add_argument("url", help="视频链接")
    parser.add_argument("--format", default="mp4", help="视频格式 (mp4/webm)")
    parser.add_argument("--output", default="downloads", help="输出目录")
    
    args = parser.parse_args()
    
    # 确保依赖
    ensure_yt_dlp()
    
    # 下载
    filepath = download_video(args.url, args.output, args.format)
    
    if filepath:
        print(f"MEDIA: {Path(filepath).resolve()}")


if __name__ == "__main__":
    main()
