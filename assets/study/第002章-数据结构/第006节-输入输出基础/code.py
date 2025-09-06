# 练习：输入输出基础

# 1. 基本输出
name = "张三"
age = 25
print(f"姓名：{name}，年龄：{age}岁")

# 2. 格式化输出
score = 95.5
print(f"成绩：{score:.1f}分")

# 3. 模拟用户输入（实际环境中会使用input()）
user_name = "李四"
user_age_str = "30"
user_score_str = "88.5"

# 4. 类型转换
user_age = int(user_age_str)
user_score = float(user_score_str)

# 5. 格式化输出用户信息
print(f"\n=== 用户信息 ===")
print(f"姓名：{user_name}")
print(f"年龄：{user_age}岁")
print(f"成绩：{user_score:.1f}分")
print("================")

# 6. 计算和输出
next_year_age = user_age + 1
print(f"明年{user_name}将{next_year_age}岁")

# 显示变量值
name
age
score
user_name
user_age
user_score
next_year_age
