# ======= 可编辑区域开始 =======

# 练习1：定义简单函数
# 定义一个函数 greet，接受一个参数 name，返回问候语
def greet(name):
    # 在这里完成函数体
    pass

# 练习2：带默认参数的函数
# 定义一个函数 calculate_area，计算矩形面积
# 参数：length（长度），width（宽度，默认值为1）
def calculate_area(length, width=1):
    # 在这里完成函数体
    pass

# 练习3：返回多个值
# 定义一个函数 get_stats，计算列表的统计信息
# 返回：总和、平均值、最大值、最小值
def get_stats(numbers):
    # 在这里完成函数体
    pass

# 练习4：可变参数
# 定义一个函数 sum_all，计算所有传入数字的和
def sum_all(*numbers):
    # 在这里完成函数体
    pass

# 练习5：Lambda 函数
# 使用 lambda 创建一个计算平方的函数
square = 

# 练习6：递归函数
# 定义一个递归函数 factorial，计算阶乘
def factorial(n):
    # 在这里完成函数体
    pass

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "greet_result": greet("张三"),
    "area_result": calculate_area(5, 3),
    "stats_result": get_stats([1, 2, 3, 4, 5]),
    "sum_result": sum_all(1, 2, 3, 4, 5),
    "square_result": square(4),
    "factorial_result": factorial(5)
}

# 学生答案
student_answer = {
    "greet_result": greet("张三"),
    "area_result": calculate_area(5, 3),
    "stats_result": get_stats([1, 2, 3, 4, 5]),
    "sum_result": sum_all(1, 2, 3, 4, 5),
    "square_result": square(4),
    "factorial_result": factorial(5)
}

# 对比答案并输出结果
student_answer == correct_answer
