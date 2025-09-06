# ======= 可编辑区域开始 =======

# 练习1：基本列表生成式
# 生成1到10的平方数列表
squares = 

# 练习2：条件过滤
# 生成1到20的偶数列表
even_numbers = 

# 生成1到10的奇数平方
odd_squares = 

# 练习3：字符串处理
# 给定字符串列表，生成所有单词的大写形式
words = ["hello", "world", "python", "programming"]
upper_words = 

# 生成长度大于5的单词
long_words = 

# 练习4：多重循环
# 生成所有可能的坐标组合 (x, y)，其中 x 和 y 都在 0-2 范围内
coordinates = 

# 生成乘法表字符串列表，格式为 "i×j=k"
multiplication_table = 

# 练习5：字典生成式
# 创建数字到其平方的映射（1到5）
squares_dict = 

# 从现有字典中过滤出值大于2的项
original_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
filtered_dict = 

# 练习6：集合生成式
# 从字符串中提取唯一字符（不包括空格）
text = "hello world"
unique_chars = 

# 生成1到10的平方数集合
squares_set = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "squares": [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
    "even_numbers": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    "odd_squares": [1, 9, 25, 49, 81],
    "upper_words": ["HELLO", "WORLD", "PYTHON", "PROGRAMMING"],
    "long_words": ["programming"],
    "coordinates": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    "multiplication_table": ["1×1=1", "1×2=2", "1×3=3", "2×1=2", "2×2=4", "2×3=6", "3×1=3", "3×2=6", "3×3=9"],
    "squares_dict": {1: 1, 2: 4, 3: 9, 4: 16, 5: 25},
    "filtered_dict": {"c": 3, "d": 4, "e": 5},
    "unique_chars": {"h", "e", "l", "o", "w", "r", "d"},
    "squares_set": {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
}

# 学生答案
student_answer = {
    "squares": squares,
    "even_numbers": even_numbers,
    "odd_squares": odd_squares,
    "upper_words": upper_words,
    "long_words": long_words,
    "coordinates": coordinates,
    "multiplication_table": multiplication_table,
    "squares_dict": squares_dict,
    "filtered_dict": filtered_dict,
    "unique_chars": unique_chars,
    "squares_set": squares_set
}

# 对比答案并输出结果
student_answer == correct_answer
