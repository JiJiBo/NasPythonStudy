# ======= 可编辑区域开始 =======

# 练习1：创建不同类型的变量
# 请给以下变量赋值：
age =  # 赋值为 20
height =  # 赋值为 1.75
name =  # 赋值为 "张三"
is_student =  # 赋值为 True

# 练习2：类型转换
# 请完成以下类型转换：
age_from_str =  # 将字符串 "25" 转换为整数
str_from_int =  # 将整数 100 转换为字符串
int_from_float =  # 将浮点数 3.14 转换为整数

# 练习3：多重赋值
# 使用一行代码给三个变量 x, y, z 分别赋值 1, 2, 3
x, y, z = 

# 练习4：类型检查
# 使用 type() 函数检查上面创建的变量的类型
age_type = 
height_type = 
name_type = 
is_student_type = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "variables": {"age": 20, "height": 1.75, "name": "张三", "is_student": True},
    "conversions": {"age_from_str": 25, "str_from_int": "100", "int_from_float": 3},
    "multiple_assignment": {"x": 1, "y": 2, "z": 3},
    "types": {"age_type": "<class 'int'>", "height_type": "<class 'float'>", "name_type": "<class 'str'>", "is_student_type": "<class 'bool'>"}
}

# 学生答案
student_answer = {
    "variables": {"age": age, "height": height, "name": name, "is_student": is_student},
    "conversions": {"age_from_str": age_from_str, "str_from_int": str_from_int, "int_from_float": int_from_float},
    "multiple_assignment": {"x": x, "y": y, "z": z},
    "types": {"age_type": str(age_type), "height_type": str(height_type), "name_type": str(name_type), "is_student_type": str(is_student_type)}
}

# 对比答案并输出结果
student_answer == correct_answer
