# ======= 可编辑区域开始 =======

# 练习1：基本迭代
# 给定列表 ["苹果", "香蕉", "橙子", "葡萄"]，使用for循环遍历并收集所有水果
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
fruit_list = 

# 练习2：索引迭代
# 使用enumerate()函数获取索引和元素
names = ["张三", "李四", "王五"]
indexed_names = 

# 练习3：字典迭代
# 给定字典 {"数学": 85, "英语": 92, "物理": 78}，完成以下操作
scores = {"数学": 85, "英语": 92, "物理": 78}

# 获取所有科目名称
subjects = 

# 获取所有分数
all_scores = 

# 获取科目和分数的对应关系
subject_scores = 

# 练习4：反向迭代
# 给定列表 [1, 2, 3, 4, 5]，反向遍历
numbers = [1, 2, 3, 4, 5]
reversed_numbers = 

# 练习5：条件迭代
# 从列表 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 中找出所有偶数
numbers_1_to_10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = 

# 练习6：同时迭代多个序列
# 使用zip()函数同时遍历姓名和年龄
names_list = ["张三", "李四", "王五"]
ages_list = [20, 25, 30]
name_age_pairs = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "fruit_list": ["苹果", "香蕉", "橙子", "葡萄"],
    "indexed_names": [(0, "张三"), (1, "李四"), (2, "王五")],
    "subjects": ["数学", "英语", "物理"],
    "all_scores": [85, 92, 78],
    "subject_scores": [("数学", 85), ("英语", 92), ("物理", 78)],
    "reversed_numbers": [5, 4, 3, 2, 1],
    "even_numbers": [2, 4, 6, 8, 10],
    "name_age_pairs": [("张三", 20), ("李四", 25), ("王五", 30)]
}

# 学生答案
student_answer = {
    "fruit_list": fruit_list,
    "indexed_names": indexed_names,
    "subjects": subjects,
    "all_scores": all_scores,
    "subject_scores": subject_scores,
    "reversed_numbers": reversed_numbers,
    "even_numbers": even_numbers,
    "name_age_pairs": name_age_pairs
}

# 对比答案并输出结果
student_answer == correct_answer
