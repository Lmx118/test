# Zhihu User Recursive Spider 🌐

基于 Python 的递归爬虫，用于爬取知乎用户的回答信息及关注者关系网络。采用 BFS 算法实现多级递归爬取，支持自定义深度和关注者数量限制。

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![DrissionPage](https://img.shields.io/badge/DrissionPage-✔-green)](https://github.com/g1879/DrissionPage)

## 功能特性 ✨
- 🌐 基于浏览器自动化（DrissionPage）实现数据抓取
- 📊 自动保存用户回答信息到 CSV 文件
- 🔍 递归爬取关注者关系网络（BFS 算法）
- ⚙️ 支持自定义爬取深度和每用户最大关注者数
- ⏳ 随机延迟机制避免反爬（5-10秒）
- 🛠️ 自动处理内容解析和异常情况

## 配置 🚀
```python
# 初始化爬虫（示例配置）
spider = ZhihuRecursiveSpider(
    max_depth=3,            # 最大递归深度（0:仅自己）
    max_followers=500000,   # 每用户最大获取关注者数
    csv_filename='D:/data/用户2.csv'  # 数据存储路径
)

# 设置初始用户
start_token = "zhuruai"     # 替换为目标用户的url_token
spider.run(start_token)
