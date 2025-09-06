# 📝 Python 网络爬虫详解

## 1. 什么是网络爬虫

**网络爬虫（Web Crawler/Spider）** 是一种自动获取网页内容的程序，它模拟浏览器行为，从互联网上抓取数据。爬虫广泛应用于数据采集、搜索引擎、价格监控、新闻聚合等领域。

## 2. 爬虫的基本原理

### 2.1 HTTP协议基础
```python
# HTTP请求的基本组成部分
# 1. 请求行：方法 + URL + 协议版本
# 2. 请求头：包含客户端信息
# 3. 请求体：POST请求的数据

# 常见的HTTP方法
# GET: 获取资源
# POST: 提交数据
# PUT: 更新资源
# DELETE: 删除资源
```

### 2.2 爬虫工作流程
1. **发送HTTP请求**：向目标网站发送请求
2. **接收响应**：获取HTML、JSON等格式的数据
3. **解析数据**：提取所需的信息
4. **存储数据**：保存到文件或数据库
5. **处理反爬**：应对验证码、IP限制等

## 3. 基础库介绍

### 3.1 requests库
```python
import requests

# 基本GET请求
response = requests.get('https://httpbin.org/get')
print(response.status_code)  # 200
print(response.text)  # 响应内容

# 带参数的GET请求
params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://httpbin.org/get', params=params)
print(response.url)  # 完整的URL

# POST请求
data = {'username': 'admin', 'password': '123456'}
response = requests.post('https://httpbin.org/post', data=data)
print(response.json())

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
response = requests.get('https://httpbin.org/headers', headers=headers)
print(response.json())
```

### 3.2 urllib库（内置）
```python
import urllib.request
import urllib.parse

# 基本请求
response = urllib.request.urlopen('https://httpbin.org/get')
print(response.read().decode('utf-8'))

# 带参数的请求
params = {'key1': 'value1', 'key2': 'value2'}
url = 'https://httpbin.org/get?' + urllib.parse.urlencode(params)
response = urllib.request.urlopen(url)
print(response.read().decode('utf-8'))

# POST请求
data = urllib.parse.urlencode({'username': 'admin'}).encode('utf-8')
request = urllib.request.Request('https://httpbin.org/post', data=data)
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
```

## 4. HTML解析

### 4.1 BeautifulSoup库
```python
from bs4 import BeautifulSoup
import requests

# 获取网页内容
response = requests.get('https://example.com')
html_content = response.text

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找元素
title = soup.find('title')
print(title.text)

# 查找所有链接
links = soup.find_all('a')
for link in links:
    print(link.get('href'))

# 使用CSS选择器
divs = soup.select('div.content')
for div in divs:
    print(div.text)

# 查找特定属性的元素
images = soup.find_all('img', src=True)
for img in images:
    print(img['src'])
```

### 4.2 lxml库
```python
from lxml import html
import requests

# 获取网页内容
response = requests.get('https://example.com')
tree = html.fromstring(response.content)

# 使用XPath查找元素
titles = tree.xpath('//title/text()')
print(titles)

# 查找所有链接
links = tree.xpath('//a/@href')
print(links)

# 查找特定class的元素
divs = tree.xpath('//div[@class="content"]')
for div in divs:
    print(div.text_content())
```

## 5. 数据提取技巧

### 5.1 正则表达式
```python
import re

# 提取邮箱地址
text = "联系邮箱：admin@example.com 或 support@test.com"
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
print(emails)  # ['admin@example.com', 'support@test.com']

# 提取电话号码
text = "电话：138-1234-5678 或 010-12345678"
phones = re.findall(r'\d{3,4}-\d{7,8}|\d{11}', text)
print(phones)  # ['138-1234-5678', '010-12345678']

# 提取HTML标签内容
html_text = '<div class="price">¥99.99</div>'
price = re.search(r'<div class="price">(.*?)</div>', html_text)
if price:
    print(price.group(1))  # ¥99.99
```

### 5.2 JSON数据提取
```python
import json
import requests

# 获取JSON数据
response = requests.get('https://api.github.com/users/octocat')
data = response.json()

# 提取特定字段
print(f"用户名: {data['login']}")
print(f"姓名: {data['name']}")
print(f"关注者: {data['followers']}")

# 处理嵌套JSON
if 'company' in data:
    print(f"公司: {data['company']}")
```

## 6. 反爬虫应对

### 6.1 设置请求头
```python
import requests
import random

# 随机User-Agent
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

response = requests.get('https://example.com', headers=headers)
```

### 6.2 使用代理
```python
import requests

# 使用代理
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

response = requests.get('https://httpbin.org/ip', proxies=proxies)
print(response.json())

# 随机代理
proxy_list = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080'
]

import random
proxy = random.choice(proxy_list)
proxies = {'http': proxy, 'https': proxy}
```

### 6.3 处理Cookie和Session
```python
import requests

# 使用Session保持Cookie
session = requests.Session()

# 登录
login_data = {'username': 'admin', 'password': '123456'}
session.post('https://example.com/login', data=login_data)

# 访问需要登录的页面
response = session.get('https://example.com/dashboard')
print(response.text)

# 手动设置Cookie
cookies = {'session_id': 'abc123', 'user_id': '456'}
response = requests.get('https://example.com', cookies=cookies)
```

### 6.4 延时和重试
```python
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 随机延时
def random_delay():
    time.sleep(random.uniform(1, 3))

# 重试机制
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# 使用
response = session.get('https://example.com')
random_delay()
```

## 7. 实际应用示例

### 7.1 新闻网站爬虫
```python
import requests
from bs4 import BeautifulSoup
import json
import time

def crawl_news(url):
    """爬取新闻列表"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = []
        # 假设新闻在class为news-item的div中
        news_items = soup.find_all('div', class_='news-item')
        
        for item in news_items:
            title_elem = item.find('h3')
            link_elem = item.find('a')
            time_elem = item.find('span', class_='time')
            
            if title_elem and link_elem:
                news = {
                    'title': title_elem.text.strip(),
                    'link': link_elem.get('href'),
                    'time': time_elem.text.strip() if time_elem else ''
                }
                news_list.append(news)
        
        return news_list
    
    except Exception as e:
        print(f"爬取失败: {e}")
        return []

# 使用示例
news_url = "https://news.example.com"
news_data = crawl_news(news_url)

# 保存到JSON文件
with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
```

### 7.2 电商价格监控
```python
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

def get_product_price(url):
    """获取商品价格"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找价格元素（根据实际网站调整选择器）
        price_elem = soup.find('span', class_='price')
        if price_elem:
            price_text = price_elem.text
            # 提取数字
            price = re.search(r'[\d,]+\.?\d*', price_text)
            if price:
                return float(price.group().replace(',', ''))
        
        return None
    
    except Exception as e:
        print(f"获取价格失败: {e}")
        return None

def monitor_price(product_url, target_price):
    """价格监控"""
    while True:
        current_price = get_product_price(product_url)
        if current_price:
            print(f"{datetime.now()}: 当前价格 {current_price}")
            
            if current_price <= target_price:
                print(f"价格达到目标！当前价格: {current_price}")
                break
        
        time.sleep(3600)  # 每小时检查一次

# 使用示例
product_url = "https://shop.example.com/product/123"
target_price = 99.99
monitor_price(product_url, target_price)
```

### 7.3 图片下载器
```python
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def download_images(url, save_dir='images'):
    """下载网页中的所有图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有图片
        img_tags = soup.find_all('img')
        
        for i, img in enumerate(img_tags):
            img_url = img.get('src')
            if img_url:
                # 处理相对URL
                img_url = urljoin(url, img_url)
                
                # 获取文件名
                parsed_url = urlparse(img_url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = f"image_{i}.jpg"
                
                # 下载图片
                try:
                    img_response = requests.get(img_url, headers=headers)
                    img_response.raise_for_status()
                    
                    filepath = os.path.join(save_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f"下载成功: {filename}")
                
                except Exception as e:
                    print(f"下载失败 {img_url}: {e}")
    
    except Exception as e:
        print(f"获取页面失败: {e}")

# 使用示例
download_images("https://example.com/gallery")
```

## 8. 数据存储

### 8.1 保存到文件
```python
import json
import csv
import pandas as pd

# 保存为JSON
data = [
    {'name': '张三', 'age': 25, 'city': '北京'},
    {'name': '李四', 'age': 30, 'city': '上海'}
]

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 保存为CSV
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])
    writer.writeheader()
    writer.writerows(data)

# 使用pandas保存
df = pd.DataFrame(data)
df.to_csv('data_pandas.csv', index=False, encoding='utf-8')
df.to_excel('data.xlsx', index=False)
```

### 8.2 保存到数据库
```python
import sqlite3
import pymongo

# SQLite数据库
def save_to_sqlite(data):
    conn = sqlite3.connect('crawled_data.db')
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 插入数据
    for item in data:
        cursor.execute('''
            INSERT INTO news (title, content, url)
            VALUES (?, ?, ?)
        ''', (item['title'], item['content'], item['url']))
    
    conn.commit()
    conn.close()

# MongoDB数据库
def save_to_mongodb(data):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['crawled_data']
    collection = db['news']
    
    collection.insert_many(data)
    client.close()
```

## 9. 爬虫框架

### 9.1 Scrapy框架
```python
# scrapy_example.py
import scrapy

class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['https://news.example.com']
    
    def parse(self, response):
        # 解析新闻列表
        for news in response.css('div.news-item'):
            yield {
                'title': news.css('h3::text').get(),
                'link': news.css('a::attr(href)').get(),
                'time': news.css('span.time::text').get()
            }
        
        # 跟进下一页
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

# 运行命令: scrapy runspider scrapy_example.py -o news.json
```

### 9.2 Selenium自动化
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def crawl_with_selenium(url):
    """使用Selenium爬取动态内容"""
    # 设置Chrome选项
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # 等待页面加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content"))
        )
        
        # 滚动加载更多内容
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # 提取数据
        elements = driver.find_elements(By.CLASS_NAME, "item")
        data = []
        for element in elements:
            title = element.find_element(By.TAG_NAME, "h3").text
            data.append({'title': title})
        
        return data
    
    finally:
        driver.quit()

# 使用示例
data = crawl_with_selenium("https://dynamic-site.example.com")
```

## 10. 法律和道德考虑

### 10.1 robots.txt协议
```python
import requests
from urllib.robotparser import RobotFileParser

def check_robots_txt(url):
    """检查robots.txt"""
    rp = RobotFileParser()
    rp.set_url(url + '/robots.txt')
    rp.read()
    
    return rp.can_fetch('*', url)

# 使用示例
if check_robots_txt('https://example.com'):
    print("允许爬取")
else:
    print("不允许爬取")
```

### 10.2 最佳实践
1. **遵守robots.txt**：尊重网站的爬虫协议
2. **控制频率**：避免对服务器造成过大压力
3. **尊重版权**：不要爬取受版权保护的内容
4. **数据使用**：合理使用爬取的数据
5. **隐私保护**：不要爬取个人隐私信息

## 重要提示

1. **遵守法律法规**：确保爬虫行为合法
2. **尊重网站规则**：遵守robots.txt和网站条款
3. **控制请求频率**：避免对服务器造成压力
4. **处理异常**：做好错误处理和重试机制
5. **数据质量**：验证和清洗爬取的数据
6. **性能优化**：使用异步请求提高效率
7. **反爬应对**：合理应对各种反爬措施

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
