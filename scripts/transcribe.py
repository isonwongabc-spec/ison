#!/usr/bin/env python3
"""
语音转文字脚本
"""

import sys
import subprocess

def transcribe(audio_path):
    try:
        import whisper
        print("正在加载模型...")
        model = whisper.load_model("turbo")
        print("正在转录...")
        result = model.transcribe(audio_path, language="zh")
        return result["text"]
    except ImportError:
        print("正在安装 whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper", "-q"])
        import whisper
        model = whisper.load_model("turbo")
        result = model.transcribe(audio_path, language="zh")
        return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python transcribe.py <音频文件>")
        sys.exit(1)
    
    text = transcribe(sys.argv[1])
    print(f"\n转录结果: {text}")
