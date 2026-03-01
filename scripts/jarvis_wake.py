import pvporcupine
import pyaudio
import struct
import os
import subprocess
import sys

class JarvisWakeWord:
    def __init__(self):
        # 使用内置的 Jarvis 唤醒词
        self.access_key = ""  # 免费版不需要 access key
        self.keyword_paths = None
        
        # 初始化 Porcupine
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keywords=["jarvis"],  # 内置唤醒词
            sensitivities=[0.8]   # 敏感度 0-1
        )
        
        # 初始化音频
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        
        print("🎙️ Jarvis 语音唤醒已启动")
        print("📢 说 'Hey Jarvis' 或 'Jarvis' 来唤醒")
        print("⛔ 按 Ctrl+C 停止\n")
    
    def run(self):
        try:
            while True:
                # 读取音频帧
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # 处理音频
                keyword_index = self.porcupine.process(pcm)
                
                # 检测到唤醒词
                if keyword_index >= 0:
                    print("✅ 检测到唤醒词: Jarvis!")
                    self.on_wake()
                    
        except KeyboardInterrupt:
            print("\n⛔ 停止监听")
        finally:
            self.cleanup()
    
    def on_wake(self):
        """唤醒后的操作"""
        # 播放提示音（可选）
        # subprocess.run(['powershell', '-c', '[console]::beep(800, 200)'])
        
        # 发送通知到 OpenClaw（通过文件触发）
        trigger_file = os.path.expanduser("~/.openclaw/workspace/memory/jarvis_wake.trigger")
        with open(trigger_file, "w") as f:
            f.write(f"waked_at: {time.time()}\n")
        
        print("🚀 Jarvis 已激活，等待指令...")
        # 这里可以触发语音输入、执行命令等
    
    def cleanup(self):
        """清理资源"""
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()

if __name__ == "__main__":
    import time
    jarvis = JarvisWakeWord()
    jarvis.run()
