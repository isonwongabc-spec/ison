import keyboard
import os
import subprocess
import time

class JarvisHotkey:
    def __init__(self):
        self.hotkey = "ctrl+alt+j"
        print("🎙️ Jarvis 快捷键模式已启动")
        print(f"📢 按 `{self.hotkey}` 唤醒 Jarvis")
        print("⛔ 按 Ctrl+C 停止\n")
    
    def on_wake(self):
        """唤醒后的操作"""
        print("✅ Jarvis 已激活!")
        
        # 播放提示音
        try:
            import winsound
            winsound.Beep(800, 200)
            winsound.Beep(1000, 200)
        except:
            pass
        
        # 创建触发文件
        trigger_file = os.path.expanduser("~/.openclaw/workspace/memory/jarvis_wake.trigger")
        with open(trigger_file, "w") as f:
            f.write(f"waked_at: {time.time()}\n")
        
        # 这里可以启动语音识别或执行命令
        print("🚀 等待指令...")
        
        # 示例：打开语音输入提示
        # subprocess.run(['python', 'jarvis_voice_input.py'])
    
    def run(self):
        """运行监听"""
        keyboard.add_hotkey(self.hotkey, self.on_wake)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ 停止监听")

if __name__ == "__main__":
    jarvis = JarvisHotkey()
    jarvis.run()
