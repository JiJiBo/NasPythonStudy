# ======= 可编辑区域开始 =======

# 练习1：条件判断
# 根据用户年龄判断是否可以投票（18岁以上可以投票）
age = 20  # 可以修改这个值来测试
vote_result =  # 根据age判断是否可以投票，赋值"可以投票"或"不能投票"

# 练习2：多条件判断
# 根据分数判断等级：90+优秀，80-89良好，70-79中等，60-69及格，60以下不及格
score = 85  # 可以修改这个值来测试
grade =  # 根据score判断等级

# 练习3：for循环
# 使用for循环收集1到10的所有数字
numbers_1_to_10 = 

# 练习4：while循环
# 使用while循环计算1到100的和
sum_result = 

# 练习5：循环控制
# 使用for循环收集1到20的奇数（使用continue跳过偶数）
odd_numbers = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "vote_result": "可以投票",
    "grade": "良好",
    "numbers_1_to_10": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "sum_1_to_100": 5050,
    "odd_numbers_1_to_20": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
}

# 学生答案
student_answer = {
    "vote_result": vote_result,
    "grade": grade,
    "numbers_1_to_10": numbers_1_to_10,
    "sum_1_to_100": sum_result,
    "odd_numbers_1_to_20": odd_numbers
}

# 对比答案并输出结果
student_answer == correct_answer
