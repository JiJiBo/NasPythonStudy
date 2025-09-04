# 输入输出基础

## 一、输出函数 print()

`print()` 函数用于将信息显示到屏幕上：

```python
# 基本输出
print("Hello World")

# 输出多个值
name = "张三"
age = 25
print("姓名：", name, "年龄：", age)

# 格式化输出
print(f"姓名：{name}，年龄：{age}岁")

# 指定分隔符
print(name, age, sep=" | ")

# 指定结束符
print("第一行", end=" ")
print("第二行")
```

## 二、输入函数 input()

`input()` 函数用于从用户获取输入：

```python
# 基本输入
name = input("请输入你的姓名：")
print("你好，", name)

# 输入数字（需要转换）
age_str = input("请输入你的年龄：")
age = int(age_str)
print(f"你今年{age}岁")

# 输入浮点数
height_str = input("请输入你的身高（米）：")
height = float(height_str)
print(f"你的身高是{height}米")
```

## 三、格式化输出

### 1. f-string（推荐）

```python
name = "张三"
age = 25
score = 95.5

# 基本格式化
print(f"姓名：{name}")

# 数字格式化
print(f"年龄：{age}岁")
print(f"成绩：{score:.1f}分")  # 保留一位小数

# 表达式
print(f"明年年龄：{age + 1}岁")
```

### 2. format() 方法

```python
name = "张三"
age = 25

# 位置参数
print("姓名：{}，年龄：{}岁".format(name, age))

# 关键字参数
print("姓名：{n}，年龄：{a}岁".format(n=name, a=age))

# 数字格式化
score = 95.5
print("成绩：{:.1f}分".format(score))
```

### 3. % 操作符（旧式）

```python
name = "张三"
age = 25
score = 95.5

print("姓名：%s，年龄：%d岁" % (name, age))
print("成绩：%.1f分" % score)
```

## 五、实际应用示例

### 1. 简单的计算器

```python
# 获取用户输入
num1_str = input("请输入第一个数字：")
num2_str = input("请输入第二个数字：")

# 转换为数字
num1 = float(num1_str)
num2 = float(num2_str)

# 计算结果
sum_result = num1 + num2
diff_result = num1 - num2
product_result = num1 * num2

# 输出结果
print(f"{num1} + {num2} = {sum_result}")
print(f"{num1} - {num2} = {diff_result}")
print(f"{num1} × {num2} = {product_result}")
```

### 2. 个人信息收集

```python
# 收集用户信息
name = input("请输入姓名：")
age_str = input("请输入年龄：")
city = input("请输入城市：")

# 转换年龄
age = int(age_str)

# 格式化输出
print("\n=== 个人信息 ===")
print(f"姓名：{name}")
print(f"年龄：{age}岁")
print(f"城市：{city}")
print("================")
```

### 3. 成绩统计

```python
# 获取三门课程成绩
math_str = input("请输入数学成绩：")
english_str = input("请输入英语成绩：")
python_str = input("请输入Python成绩：")

# 转换为数字
math = float(math_str)
english = float(english_str)
python = float(python_str)

# 计算平均分
average = (math + english + python) / 3

# 输出结果
print(f"\n数学：{math}分")
print(f"英语：{english}分")
print(f"Python：{python}分")
print(f"平均分：{average:.2f}分")
```

## 注意事项

- `input()` 总是返回字符串，需要手动转换
- f-string 是Python 3.6+的推荐格式化方式
- 注意输入验证，确保程序稳定性
- 格式化输出时注意数字精度控制
