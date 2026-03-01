---
name: news-summarizer
description: 抓取热点新闻并生成摘要。当用户说"今天有什么新闻"、"帮我总结热点"或需要新闻摘要时使用。
---

# News Summarizer

## 使用方式

```bash
# 获取今日热点新闻
python {baseDir}/scripts/summarize.py

# 指定分类
python {baseDir}/scripts/summarize.py --category tech
```

## 支持的分类

- `tech` - 科技
- `finance` - 财经
- `sports` - 体育
- `all` - 全部 (默认)

## 输出

- 新闻标题 + 摘要
- 原文链接
