#!/usr/bin/env python3
"""
OKX 桌面软件自动化脚本
依赖: pyautogui, pillow
"""

import argparse
import subprocess
import sys
import time
import os


def ensure_pyautogui():
    """确保 pyautogui 已安装"""
    try:
        import pyautogui
    except ImportError:
        print("正在安装 pyautogui...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui", "pillow", "-q"], check=True)


def launch_okx():
    """启动 OKX"""
    okx_path = "D:\\okx\\OKX.exe"
    
    # 检查是否已在运行
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if 'OKX' in proc.info['name']:
                print("OKX 已在运行")
                return True
    except:
        pass
    
    if os.path.exists(okx_path):
        print("正在启动 OKX...")
        subprocess.Popen([okx_path], shell=True)
        time.sleep(5)  # 等待启动
        return True
    else:
        print(f"未找到 OKX: {okx_path}")
        return False


def find_and_click(image_name, confidence=0.8):
    """在屏幕上查找并点击图像"""
    import pyautogui
    
    # 这里需要实际的截图文件
    # 暂时用坐标点击
    pass


def navigate_to_trading(pair, trade_type):
    """导航到交易界面"""
    import pyautogui
    
    print(f"正在导航到 {pair} {trade_type} 界面...")
    
    # 确保窗口在最前
    pyautogui.keyDown('alt')
    pyautogui.keyDown('tab')
    pyautogui.keyUp('tab')
    pyautogui.keyUp('alt')
    time.sleep(0.5)
    
    # 点击交易菜单 (坐标需要根据实际屏幕调整)
    # 这些是示例坐标，需要根据实际情况校准
    screen_width, screen_height = pyautogui.size()
    
    # 假设交易按钮在左侧菜单
    trade_button_x = 100
    trade_button_y = 200
    
    print("点击交易菜单...")
    pyautogui.click(trade_button_x, trade_button_y)
    time.sleep(1)
    
    # 点击合约/现货
    if trade_type == "swap":
        print("点击合约...")
        # 合约按钮坐标
        pyautogui.click(200, 300)
    else:
        print("点击现货...")
        pyautogui.click(200, 250)
    time.sleep(1)
    
    # 搜索币种
    print(f"搜索 {pair}...")
    pyautogui.click(400, 150)  # 搜索框坐标
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite(pair)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)
    
    print("导航完成！")


def main():
    parser = argparse.ArgumentParser(description="OKX 自动化")
    parser.add_argument("--pair", default="BTC", help="交易对 (BTC, ETH, SOL)")
    parser.add_argument("--type", default="swap", choices=["swap", "spot"], help="交易类型")
    
    args = parser.parse_args()
    
    ensure_pyautogui()
    
    if launch_okx():
        if args.pair:
            navigate_to_trading(args.pair.upper(), args.type)
        print("✅ 完成！")
    else:
        print("❌ 启动失败")


if __name__ == "__main__":
    main()
