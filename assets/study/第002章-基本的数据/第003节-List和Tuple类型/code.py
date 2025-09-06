# ======= 可编辑区域开始 =======

# 练习1：列表基本操作
# 创建一个包含5个水果的列表，然后：
# 1. 在末尾添加"葡萄"
# 2. 在第二个位置插入"草莓"
# 3. 删除第一个元素
# 4. 保存最终列表
fruits = ["苹果", "香蕉", "橙子", "桃子", "梨"]
# 在这里完成列表操作
final_fruits = 

# 练习2：列表推导式
# 使用列表推导式创建一个包含1到10的平方数的列表
squares = 

# 练习3：元组操作
# 创建一个包含学生信息的元组：(姓名, 年龄, 成绩)
# 然后解包这个元组
student = ("张三", 20, 85)
name, age, score = 

# 练习4：嵌套结构
# 创建一个包含多个学生信息的列表，每个学生信息是一个元组
# 然后遍历这个列表并收集学生信息
students = [
    ("李四", 19, 92),
    ("王五", 21, 78),
    ("赵六", 20, 88)
]
student_info_list = 

# 练习5：列表统计
# 给定一个数字列表，计算：
# 1. 总和
# 2. 平均值
# 3. 最大值和最小值
numbers = [45, 23, 78, 12, 67, 89, 34, 56]
total = 
average = 
maximum = 
minimum = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "final_fruits": ["草莓", "香蕉", "橙子", "桃子", "梨", "葡萄"],
    "squares": [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
    "student_info": {"name": "张三", "age": 20, "score": 85},
    "all_students": [{"name": "李四", "age": 19, "score": 92}, {"name": "王五", "age": 21, "score": 78}, {"name": "赵六", "age": 20, "score": 88}],
    "statistics": {"total": 504, "average": 63.0, "maximum": 89, "minimum": 12}
}

# 学生答案
student_answer = {
    "final_fruits": final_fruits,
    "squares": squares,
    "student_info": {"name": name, "age": age, "score": score},
    "all_students": student_info_list,
    "statistics": {"total": total, "average": round(average, 2), "maximum": maximum, "minimum": minimum}
}

# 对比答案并输出结果
student_answer == correct_answer
