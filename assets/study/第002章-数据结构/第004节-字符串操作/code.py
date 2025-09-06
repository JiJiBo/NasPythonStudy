# 练习：字符串操作

# 1. 字符串长度和索引
text = "Python编程"
length = len(text)
first_char = text[0]
last_char = text[-1]

# 2. 字符串切片
sliced_text = text[0:6]  # 获取前6个字符
reversed_text = text[::-1]  # 反转字符串

# 3. 字符串方法
upper_text = text.upper()
lower_text = text.lower()

# 4. 字符串分割和拼接
sentence = "Python,Java,C++"
languages = sentence.split(",")
joined_text = " ".join(languages)

# 5. 字符串查找和替换
has_python = "Python" in text
replaced_text = text.replace("编程", "学习")

# 显示所有结果
length
first_char
last_char
sliced_text
reversed_text
upper_text
lower_text
languages
joined_text
has_python
replaced_text
