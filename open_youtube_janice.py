import subprocess
import time
import sys

def open_youtube_and_search():
    """打开YouTube并搜索卫兰歌曲"""
    
    # 使用默认浏览器打开YouTube搜索结果
    youtube_url = "https://www.youtube.com/results?search_query=%E5%8D%AB%E5%85%B0+%E6%AD%8C%E6%9B%B2"
    
    print("正在打开YouTube搜索卫兰歌曲...")
    
    # Windows上打开默认浏览器
    subprocess.run(['start', '', youtube_url], shell=True)
    
    print("OK - 已打开浏览器，搜索: 卫兰 歌曲")
    print("请在搜索结果中选择想听的歌曲播放")

if __name__ == "__main__":
    open_youtube_and_search()