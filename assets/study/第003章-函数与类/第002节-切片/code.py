# ======= 可编辑区域开始 =======

# 练习1：字符串切片
# 给定字符串 "Python Programming"，完成以下切片操作
text = "Python Programming"

# 获取前6个字符
first_six = 

# 获取后11个字符
last_eleven = 

# 获取中间部分 "Programming"
middle_part = 

# 反向切片
reversed_text = 

# 练习2：列表切片
# 给定列表 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]，完成以下操作
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 获取前5个元素
first_five = 

# 获取后5个元素
last_five = 

# 获取中间部分 [2, 3, 4, 5, 6]
middle_numbers = 

# 每隔一个元素取一个
every_other = 

# 练习3：负索引切片
# 给定字符串 "Hello World"，使用负索引完成切片
hello_world = "Hello World"

# 获取最后5个字符
last_five_chars = 

# 获取除了最后2个字符外的所有字符
except_last_two = 

# 获取倒数第3个到倒数第1个字符
last_three_to_one = 

# 练习4：步长切片
# 给定列表 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]，完成以下操作
numbers_1_to_10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 每隔2个元素取一个
every_two = 

# 从索引1开始，每隔2个取一个
from_index_one = 

# 反向每隔2个取一个
reverse_every_two = 

# 练习5：文件路径处理
# 给定文件路径 "/home/user/documents/file.txt"，提取各部分
file_path = "/home/user/documents/file.txt"

# 提取文件名 "file.txt"
filename = 

# 提取目录路径 "/home/user/documents"
directory = 

# 提取文件扩展名 "txt"
extension = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "first_six": "Python",
    "last_eleven": "Programming",
    "middle_part": "Programming",
    "reversed_text": "gnimmargorP nohtyP",
    "first_five": [0, 1, 2, 3, 4],
    "last_five": [5, 6, 7, 8, 9],
    "middle_numbers": [2, 3, 4, 5, 6],
    "every_other": [0, 2, 4, 6, 8],
    "last_five_chars": "World",
    "except_last_two": "Hello Wor",
    "last_three_to_one": "rld",
    "every_two": [1, 3, 5, 7, 9],
    "from_index_one": [2, 4, 6, 8, 10],
    "reverse_every_two": [10, 8, 6, 4, 2],
    "filename": "file.txt",
    "directory": "/home/user/documents",
    "extension": "txt"
}

# 学生答案
student_answer = {
    "first_six": first_six,
    "last_eleven": last_eleven,
    "middle_part": middle_part,
    "reversed_text": reversed_text,
    "first_five": first_five,
    "last_five": last_five,
    "middle_numbers": middle_numbers,
    "every_other": every_other,
    "last_five_chars": last_five_chars,
    "except_last_two": except_last_two,
    "last_three_to_one": last_three_to_one,
    "every_two": every_two,
    "from_index_one": from_index_one,
    "reverse_every_two": reverse_every_two,
    "filename": filename,
    "directory": directory,
    "extension": extension
}

# 对比答案并输出结果
student_answer == correct_answer
