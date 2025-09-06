# 练习：类型转换

# 1. 字符串转数字
age_str = "25"
age = int(age_str)
height_str = "175.5"
height = float(height_str)

# 2. 数字转字符串
score = 95
score_str = str(score)
pi = 3.14159
pi_str = str(pi)

# 3. 布尔值转换
num1 = 0
num2 = 10
bool1 = bool(num1)
bool2 = bool(num2)

# 4. 实际应用：用户输入处理
user_age = "18"
user_score = "85.5"
age_num = int(user_age)
score_num = float(user_score)

# 5. 字符串拼接中的类型转换
name = "张三"
message = name + "今年" + str(age_num) + "岁，成绩" + str(score_num) + "分"

# 6. 数据验证示例
user_input = "123"
if user_input.isdigit():
    number = int(user_input)
    print(f"有效数字：{number}")

# 显示所有结果
age
height
score_str
pi_str
bool1
bool2
age_num
score_num
message
number
