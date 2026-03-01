---
name: ppt-generator
description: 根据主题自动生成 PPT 文件。当用户说"帮我做个关于 XX 的 PPT"、"生成演示文稿"或需要提供 PPT 时使用。
---

# PPT Generator

## 使用方式

```bash
# 生成 PPT
python {baseDir}/scripts/generate.py "人工智能的发展趋势" --pages 10

# 自定义风格
python {baseDir}/scripts/generate.py "主题" --pages 10 --style business
```

## 支持的样式

- `business` - 商务风格
- `academic` - 学术风格
- `simple` - 简约风格

## 输出

- `.pptx` 文件保存在当前目录
- 自动命名: `YYYY-MM-DD-主题.pptx`
