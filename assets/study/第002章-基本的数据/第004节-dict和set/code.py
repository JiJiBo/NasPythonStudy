# ======= 可编辑区域开始 =======

# 练习1：字典基本操作
# 创建一个学生信息字典，包含姓名、年龄、成绩
# 然后添加一个新的键值对：专业="计算机科学"
# 最后修改年龄为21
student = {"name": "张三", "age": 20, "grade": 85}
# 在这里完成字典操作

# 练习2：集合去重
# 给定一个包含重复元素的列表，使用集合去重
numbers = [1, 2, 2, 3, 3, 4, 5, 5, 6]
unique_numbers = 

# 练习3：字典推导式
# 使用字典推导式创建一个数字到其平方的映射（1到5）
squares_dict = 

# 练习4：集合运算
# 给定两个集合，计算它们的交集
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
intersection = 

# 练习5：嵌套字典访问
# 创建一个嵌套字典，然后访问嵌套的值
nested_dict = {
    "student": {
        "info": {"name": "李四", "age": 19},
        "grades": {"math": 90, "english": 88}
    }
}
student_name = 
math_grade = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "student_info": {"name": "张三", "age": 21, "grade": 85, "major": "计算机科学"},
    "unique_numbers": [1, 2, 3, 4, 5, 6],
    "squares": {1: 1, 2: 4, 3: 9, 4: 16, 5: 25},
    "intersection": [4, 5],
    "nested_access": {"name": "李四", "math_grade": 90}
}

# 学生答案
student_answer = {
    "student_info": student,
    "unique_numbers": list(unique_numbers),
    "squares": squares_dict,
    "intersection": list(intersection),
    "nested_access": {"name": student_name, "math_grade": math_grade}
}

# 对比答案并输出结果
student_answer == correct_answer
