# ======= 可编辑区域开始 =======

# 练习1：文件写入
# 创建一个名为"test.txt"的文件，写入内容"Hello, Python IO!"
with open('test.txt', 'w', encoding='utf-8') as file:
    # 请在这里写入内容
    pass

# 练习2：文件读取
# 读取刚才创建的test.txt文件内容
with open('test.txt', 'r', encoding='utf-8') as file:
    # 请在这里读取文件内容
    file_content = 

# 练习3：追加内容
# 向test.txt文件追加一行内容"这是追加的内容"
with open('test.txt', 'a', encoding='utf-8') as file:
    # 请在这里追加内容
    pass

# 练习4：逐行读取
# 创建一个包含多行的文件data.txt
lines_data = ["第一行\n", "第二行\n", "第三行\n"]
with open('data.txt', 'w', encoding='utf-8') as file:
    file.writelines(lines_data)

# 读取data.txt文件的所有行
with open('data.txt', 'r', encoding='utf-8') as file:
    # 请在这里读取所有行
    all_lines = 

# 练习5：JSON文件操作
import json

# 创建一个字典数据
data = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

# 将数据写入JSON文件
with open('data.json', 'w', encoding='utf-8') as file:
    # 请在这里写入JSON数据
    pass

# 从JSON文件读取数据
with open('data.json', 'r', encoding='utf-8') as file:
    # 请在这里读取JSON数据
    json_data = 

# 练习6：文件信息获取
import os
from pathlib import Path

# 检查test.txt文件是否存在
file_exists = 

# 获取test.txt文件的大小（字节）
file_size = 

# 获取当前工作目录
current_directory = 

# 练习7：异常处理
# 尝试读取一个不存在的文件，并处理异常
try:
    with open('nonexistent.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    error_occurred = False
except FileNotFoundError:
    error_occurred = True
    error_message = "文件不存在"

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "file_content": "Hello, Python IO!",
    "all_lines": ["第一行\n", "第二行\n", "第三行\n"],
    "json_data": {"name": "张三", "age": 25, "city": "北京"},
    "file_exists": True,
    "file_size": "大于0的整数",
    "current_directory": "包含路径的字符串",
    "error_occurred": True,
    "error_message": "文件不存在"
}

# 学生答案
student_answer = {
    "file_content": file_content if 'file_content' in locals() else None,
    "all_lines": all_lines if 'all_lines' in locals() else None,
    "json_data": json_data if 'json_data' in locals() else None,
    "file_exists": file_exists if 'file_exists' in locals() else None,
    "file_size": file_size if isinstance(file_size, int) and file_size > 0 else None,
    "current_directory": current_directory if 'current_directory' in locals() else None,
    "error_occurred": error_occurred if 'error_occurred' in locals() else None,
    "error_message": error_message if 'error_message' in locals() else None
}

# 对比答案并输出结果
student_answer == correct_answer