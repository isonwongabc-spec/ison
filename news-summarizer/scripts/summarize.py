#!/usr/bin/env python3
"""
新闻摘要脚本
依赖: feedparser, requests
"""

import argparse
import sys
import subprocess
from datetime import datetime


def ensure_deps():
    """确保依赖已安装"""
    try:
        import feedparser
        import requests
    except ImportError:
        print("正在安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "feedparser", "requests", "-q"], check=True)


def fetch_news(category="all"):
    """获取新闻"""
    import feedparser
    import requests
    
    # RSS 源配置
    feeds = {
        "tech": [
            "https://www.techcrunch.com/feed/",
            "https://feeds.arstechnica.com/arstechnica/index",
        ],
        "finance": [
            "https://feeds.bbci.co.uk/news/business/rss.xml",
            "https://www.ft.com/?format=rss",
        ],
        "general": [
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best",
        ]
    }
    
    # 中文新闻源 (如果需要)
    chinese_feeds = {
        "tech": ["https://www.36kr.com/feed"],
        "finance": ["https://www.cebnet.com.cn/rss/rss.xml"],
    }
    
    print(f"📰 正在获取新闻... ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"{'='*60}\n")
    
    news_items = []
    
    # 选择要抓取的内容
    categories_to_fetch = [category] if category != "all" else ["tech", "finance", "general"]
    
    for cat in categories_to_fetch:
        if cat in feeds:
            for feed_url in feeds[cat]:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:5]:  # 每个源取前5条
                        news_items.append({
                            "title": entry.get('title', 'No title'),
                            "summary": entry.get('summary', entry.get('description', ''))[:200] + "...",
                            "link": entry.get('link', ''),
                            "published": entry.get('published', 'Unknown'),
                            "category": cat
                        })
                except Exception as e:
                    print(f"   ⚠️  无法获取 {feed_url}: {e}")
    
    # 显示结果
    if not news_items:
        print("❌ 暂时无法获取新闻")
        return
    
    # 按分类显示
    cat_names = {"tech": "🚀 科技", "finance": "💰 财经", "general": "📰 综合"}
    
    for cat in categories_to_fetch:
        cat_news = [n for n in news_items if n["category"] == cat]
        if cat_news:
            print(f"{cat_names.get(cat, cat)}")
            print("-" * 60)
            for i, item in enumerate(cat_news[:5], 1):
                print(f"{i}. {item['title']}")
                print(f"   {item['summary'][:150]}...")
                print(f"   🔗 {item['link']}")
                print()
            print()
    
    print(f"{'='*60}")
    print(f"✅ 共获取 {len(news_items)} 条新闻")


def main():
    parser = argparse.ArgumentParser(description="新闻摘要")
    parser.add_argument("--category", default="all", 
                        choices=["all", "tech", "finance", "sports"],
                        help="新闻分类")
    
    args = parser.parse_args()
    
    ensure_deps()
    fetch_news(args.category)


if __name__ == "__main__":
    main()
