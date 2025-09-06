# 📝 Python IO操作详解

## 1. 什么是IO操作

**IO（Input/Output）** 操作是指程序与外部环境进行数据交换的过程。在Python中，IO操作主要包括：
- **文件读写**：与文件系统交互
- **标准输入输出**：与用户交互
- **网络IO**：通过网络传输数据
- **数据库IO**：与数据库交互

## 2. 文件操作基础

### 2.1 文件打开和关闭
```python
# 基本文件操作
file = open('example.txt', 'r')  # 打开文件
content = file.read()            # 读取内容
file.close()                     # 关闭文件

# 使用with语句（推荐）
with open('example.txt', 'r') as file:
    content = file.read()
# 文件会自动关闭
```

### 2.2 文件打开模式
```python
# 读取模式
with open('file.txt', 'r') as f:    # 文本读取
    content = f.read()

with open('file.txt', 'rb') as f:   # 二进制读取
    content = f.read()

# 写入模式
with open('file.txt', 'w') as f:    # 文本写入（覆盖）
    f.write('Hello World')

with open('file.txt', 'a') as f:    # 追加模式
    f.write('New Line')

# 读写模式
with open('file.txt', 'r+') as f:   # 读写模式
    content = f.read()
    f.write('Additional content')
```

## 3. 文本文件操作

### 3.1 读取文本文件
```python
# 读取整个文件
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)

# 逐行读取
with open('example.txt', 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())  # strip()去除换行符

# 读取所有行到列表
with open('example.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    print(lines)

# 读取指定字符数
with open('example.txt', 'r', encoding='utf-8') as file:
    chunk = file.read(100)  # 读取100个字符
    print(chunk)
```

### 3.2 写入文本文件
```python
# 写入字符串
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write('Hello, World!')

# 写入多行
lines = ['第一行\n', '第二行\n', '第三行\n']
with open('output.txt', 'w', encoding='utf-8') as file:
    file.writelines(lines)

# 追加内容
with open('output.txt', 'a', encoding='utf-8') as file:
    file.write('追加的内容\n')
```

### 3.3 文件位置操作
```python
with open('example.txt', 'r+', encoding='utf-8') as file:
    # 获取当前位置
    position = file.tell()
    print(f"当前位置: {position}")
    
    # 移动到文件开头
    file.seek(0)
    
    # 移动到文件末尾
    file.seek(0, 2)
    
    # 相对位置移动
    file.seek(10, 1)  # 从当前位置向后移动10个字符
```

## 4. 二进制文件操作

### 4.1 读取二进制文件
```python
# 读取图片文件
with open('image.jpg', 'rb') as file:
    image_data = file.read()
    print(f"图片大小: {len(image_data)} 字节")

# 分块读取大文件
def read_large_file(filename, chunk_size=1024):
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 使用生成器读取大文件
for chunk in read_large_file('large_file.bin'):
    process_chunk(chunk)
```

### 4.2 写入二进制文件
```python
# 写入二进制数据
data = b'\x48\x65\x6c\x6c\x6f'  # "Hello"的字节表示
with open('binary_file.bin', 'wb') as file:
    file.write(data)

# 复制文件
def copy_file(source, destination):
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        while True:
            chunk = src.read(4096)  # 4KB块
            if not chunk:
                break
            dst.write(chunk)

copy_file('source.txt', 'destination.txt')
```

## 5. CSV文件操作

### 5.1 使用csv模块
```python
import csv

# 读取CSV文件
with open('data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# 读取CSV文件（字典格式）
with open('data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['name'], row['age'])

# 写入CSV文件
data = [
    ['姓名', '年龄', '城市'],
    ['张三', '25', '北京'],
    ['李四', '30', '上海']
]

with open('output.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

### 5.2 使用pandas处理CSV
```python
import pandas as pd

# 读取CSV文件
df = pd.read_csv('data.csv')
print(df.head())

# 写入CSV文件
df.to_csv('output.csv', index=False, encoding='utf-8')
```

## 6. JSON文件操作

### 6.1 使用json模块
```python
import json

# 读取JSON文件
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    print(data)

# 写入JSON文件
data = {
    'name': '张三',
    'age': 25,
    'city': '北京',
    'hobbies': ['读书', '游泳', '编程']
}

with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

# JSON字符串操作
json_string = '{"name": "李四", "age": 30}'
data = json.loads(json_string)
print(data['name'])

# 对象转JSON字符串
data = {'name': '王五', 'age': 28}
json_string = json.dumps(data, ensure_ascii=False)
print(json_string)
```

## 7. 标准输入输出

### 7.1 标准输入
```python
# 读取用户输入
name = input("请输入您的姓名: ")
print(f"您好, {name}!")

# 读取多行输入
print("请输入多行文本（输入空行结束）:")
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

print("您输入的内容:")
for line in lines:
    print(line)
```

### 7.2 标准输出
```python
# 基本输出
print("Hello, World!")

# 格式化输出
name = "张三"
age = 25
print(f"姓名: {name}, 年龄: {age}")

# 多个参数
print("姓名:", name, "年龄:", age)

# 指定分隔符
print("a", "b", "c", sep="-")  # 输出: a-b-c

# 指定结束符
print("Hello", end=" ")
print("World")  # 输出: Hello World
```

### 7.3 重定向输入输出
```python
import sys

# 重定向标准输出到文件
with open('output.txt', 'w') as f:
    sys.stdout = f
    print("这行文字会写入文件")
    sys.stdout = sys.__stdout__  # 恢复标准输出

# 从文件读取输入
with open('input.txt', 'r') as f:
    sys.stdin = f
    content = input()  # 从文件读取
    sys.stdin = sys.__stdin__  # 恢复标准输入
```

## 8. 文件系统操作

### 8.1 使用os模块
```python
import os

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")

# 改变工作目录
os.chdir('/path/to/directory')

# 列出目录内容
files = os.listdir('.')
print(f"目录内容: {files}")

# 创建目录
os.makedirs('new_directory', exist_ok=True)

# 删除文件
os.remove('file_to_delete.txt')

# 删除目录
os.rmdir('empty_directory')

# 检查文件是否存在
if os.path.exists('file.txt'):
    print("文件存在")
```

### 8.2 使用pathlib模块（推荐）
```python
from pathlib import Path

# 创建Path对象
path = Path('example.txt')

# 检查文件是否存在
if path.exists():
    print("文件存在")

# 获取文件信息
print(f"文件名: {path.name}")
print(f"文件扩展名: {path.suffix}")
print(f"父目录: {path.parent}")
print(f"绝对路径: {path.absolute()}")

# 创建目录
Path('new_directory').mkdir(exist_ok=True)

# 遍历目录
for file_path in Path('.').iterdir():
    if file_path.is_file():
        print(f"文件: {file_path.name}")
    elif file_path.is_dir():
        print(f"目录: {file_path.name}")

# 读取文件
content = Path('example.txt').read_text(encoding='utf-8')

# 写入文件
Path('output.txt').write_text('Hello, World!', encoding='utf-8')
```

## 9. 异常处理

### 9.1 文件操作异常
```python
try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("文件不存在")
except PermissionError:
    print("没有权限访问文件")
except UnicodeDecodeError:
    print("文件编码错误")
except Exception as e:
    print(f"其他错误: {e}")
```

### 9.2 安全的文件操作
```python
def safe_read_file(filename):
    """安全地读取文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except PermissionError:
        print(f"没有权限读取文件 {filename}")
        return None
    except UnicodeDecodeError:
        print(f"文件 {filename} 编码错误")
        return None

# 使用安全读取函数
content = safe_read_file('example.txt')
if content:
    print(content)
```

## 10. 实际应用示例

### 10.1 日志文件处理
```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 使用日志
logging.info("应用程序启动")
logging.warning("这是一个警告")
logging.error("这是一个错误")
```

### 10.2 配置文件处理
```python
import configparser

# 创建配置文件
config = configparser.ConfigParser()
config['DATABASE'] = {
    'host': 'localhost',
    'port': '3306',
    'username': 'admin',
    'password': 'secret'
}

config['API'] = {
    'base_url': 'https://api.example.com',
    'timeout': '30'
}

# 写入配置文件
with open('config.ini', 'w') as configfile:
    config.write(configfile)

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

db_host = config['DATABASE']['host']
api_url = config['API']['base_url']
```

### 10.3 数据备份脚本
```python
import shutil
from pathlib import Path
from datetime import datetime

def backup_file(source, backup_dir):
    """备份文件"""
    source_path = Path(source)
    if not source_path.exists():
        print(f"源文件 {source} 不存在")
        return False
    
    # 创建备份目录
    backup_path = Path(backup_dir)
    backup_path.mkdir(exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_path.stem}_{timestamp}{source_path.suffix}"
    backup_file = backup_path / backup_name
    
    # 复制文件
    shutil.copy2(source_path, backup_file)
    print(f"文件已备份到: {backup_file}")
    return True

# 使用备份函数
backup_file('important_data.txt', 'backups')
```

## 重要提示

1. **使用with语句**：确保文件正确关闭
2. **指定编码**：处理中文等非ASCII字符
3. **异常处理**：处理文件不存在、权限等错误
4. **路径处理**：使用pathlib处理路径
5. **大文件处理**：分块读取避免内存溢出
6. **安全考虑**：验证文件路径，防止路径遍历攻击
7. **性能优化**：合理使用缓冲区和批量操作

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
