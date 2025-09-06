# ======= 可编辑区域开始 =======

# 练习1：基本HTTP请求
import requests

# 发送GET请求到httpbin.org
response = requests.get('https://httpbin.org/get')
# 请获取响应的状态码
status_code = 

# 请获取响应的JSON数据
json_data = 

# 练习2：带参数的请求
# 发送带查询参数的GET请求
params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://httpbin.org/get', params=params)
# 请获取完整的URL
full_url = 

# 练习3：设置请求头
# 设置User-Agent请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get('https://httpbin.org/headers', headers=headers)
# 请获取响应中的headers信息
response_headers = 

# 练习4：POST请求
# 发送POST请求
data = {'username': 'admin', 'password': '123456'}
response = requests.post('https://httpbin.org/post', data=data)
# 请获取POST请求的form数据
form_data = 

# 练习5：HTML解析
from bs4 import BeautifulSoup

# 创建一个简单的HTML字符串
html_content = '''
<html>
<head><title>测试页面</title></head>
<body>
    <div class="content">
        <h1>标题</h1>
        <p>这是一个段落</p>
        <a href="https://example.com">链接</a>
    </div>
</body>
</html>
'''

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')
# 请获取页面标题
page_title = 

# 请获取所有链接的href属性
links = 

# 练习6：CSS选择器
# 使用CSS选择器查找class为content的div
content_div = 

# 请获取该div中的文本内容
content_text = 

# 练习7：正则表达式提取
import re

# 从文本中提取邮箱地址
text = "联系邮箱：admin@example.com 或 support@test.com"
# 请使用正则表达式提取所有邮箱地址
emails = 

# 从文本中提取电话号码
phone_text = "电话：138-1234-5678 或 010-12345678"
# 请使用正则表达式提取所有电话号码
phones = 

# 练习8：JSON数据处理
# 创建一个JSON字符串
json_string = '{"name": "张三", "age": 25, "city": "北京", "hobbies": ["读书", "游泳"]}'
# 请解析JSON字符串
parsed_json = 

# 请获取name字段的值
name_value = 

# 请获取hobbies列表
hobbies_list = 

# 练习9：异常处理
# 尝试访问一个不存在的URL
try:
    response = requests.get('https://httpbin.org/status/404')
    # 请检查响应状态码是否为404
    is_404 = 
    error_occurred = False
except requests.exceptions.RequestException as e:
    error_occurred = True
    error_message = str(e)

# 练习10：Session使用
# 创建Session对象
session = requests.Session()
# 设置Session的headers
session.headers.update({'User-Agent': 'MyBot/1.0'})
# 使用Session发送请求
response = session.get('https://httpbin.org/headers')
# 请获取响应中的User-Agent
user_agent = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "status_code": 200,
    "json_data": "包含args等字段的字典",
    "full_url": "https://httpbin.org/get?key1=value1&key2=value2",
    "response_headers": "包含User-Agent的字典",
    "form_data": {"username": "admin", "password": "123456"},
    "page_title": "测试页面",
    "links": ["https://example.com"],
    "content_text": "标题\n这是一个段落\n链接",
    "emails": ["admin@example.com", "support@test.com"],
    "phones": ["138-1234-5678", "010-12345678"],
    "name_value": "张三",
    "hobbies_list": ["读书", "游泳"],
    "is_404": True,
    "error_occurred": False,
    "user_agent": "MyBot/1.0"
}

# 学生答案
student_answer = {
    "status_code": status_code if 'status_code' in locals() else None,
    "json_data": str(type(json_data)) if 'json_data' in locals() else None,
    "full_url": full_url if 'full_url' in locals() else None,
    "response_headers": str(type(response_headers)) if 'response_headers' in locals() else None,
    "form_data": form_data if 'form_data' in locals() else None,
    "page_title": page_title if 'page_title' in locals() else None,
    "links": links if 'links' in locals() else None,
    "content_text": content_text if 'content_text' in locals() else None,
    "emails": emails if 'emails' in locals() else None,
    "phones": phones if 'phones' in locals() else None,
    "name_value": name_value if 'name_value' in locals() else None,
    "hobbies_list": hobbies_list if 'hobbies_list' in locals() else None,
    "is_404": is_404 if 'is_404' in locals() else None,
    "error_occurred": error_occurred if 'error_occurred' in locals() else None,
    "user_agent": user_agent if 'user_agent' in locals() else None
}

# 对比答案并输出结果
student_answer == correct_answer