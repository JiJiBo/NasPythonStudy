# 🔄 Python 条件判断与循环详解

## 1. 条件判断 (if-elif-else)

### 1.1 基本语法
```python
if 条件:
    执行语句
elif 条件:
    执行语句
else:
    执行语句
```

### 1.2 简单示例
```python
age = 18

if age >= 18:
    print("成年人")
else:
    print("未成年人")
```

### 1.3 多条件判断
```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 70:
    print("中等")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

### 1.4 逻辑运算符
```python
# and (与)
if age >= 18 and score >= 60:
    print("成年人且及格")

# or (或)
if age < 18 or age > 65:
    print("特殊年龄段")

# not (非)
if not is_student:
    print("不是学生")
```

### 1.5 比较运算符
```python
# 等于
if x == 10:
    print("x等于10")

# 不等于
if x != 10:
    print("x不等于10")

# 大于、小于
if x > 5:
    print("x大于5")

if x < 20:
    print("x小于20")

# 大于等于、小于等于
if x >= 10:
    print("x大于等于10")

if x <= 20:
    print("x小于等于20")
```

## 2. 循环结构

### 2.1 for 循环

#### 基本语法
```python
for 变量 in 序列:
    执行语句
```

#### 遍历列表
```python
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢{fruit}")
```

#### 遍历字符串
```python
name = "Python"
for char in name:
    print(char)
```

#### 使用 range() 函数
```python
# 生成 0 到 4 的数字
for i in range(5):
    print(i)

# 生成 1 到 10 的数字
for i in range(1, 11):
    print(i)

# 生成 0 到 10 的偶数
for i in range(0, 11, 2):
    print(i)
```

#### 遍历字典
```python
student = {"name": "张三", "age": 20, "grade": "A"}

# 遍历键
for key in student:
    print(key)

# 遍历键值对
for key, value in student.items():
    print(f"{key}: {value}")
```

### 2.2 while 循环

#### 基本语法
```python
while 条件:
    执行语句
```

#### 简单示例
```python
count = 0
while count < 5:
    print(f"计数: {count}")
    count += 1
```

#### 用户输入循环
```python
while True:
    user_input = input("请输入一个数字 (输入 'quit' 退出): ")
    if user_input == 'quit':
        break
    print(f"你输入了: {user_input}")
```

## 3. 循环控制语句

### 3.1 break - 跳出循环
```python
for i in range(10):
    if i == 5:
        break  # 当 i 等于 5 时跳出循环
    print(i)
```

### 3.2 continue - 跳过当前迭代
```python
for i in range(10):
    if i % 2 == 0:
        continue  # 跳过偶数
    print(i)  # 只打印奇数
```

### 3.3 pass - 占位符
```python
for i in range(5):
    if i == 2:
        pass  # 什么都不做，继续执行
    print(i)
```

## 4. 嵌套循环

### 4.1 嵌套 for 循环
```python
# 打印乘法表
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} × {j} = {i * j}")
```

### 4.2 嵌套条件判断
```python
for i in range(1, 6):
    if i % 2 == 0:
        if i == 4:
            print("找到数字4")
        else:
            print(f"偶数: {i}")
    else:
        print(f"奇数: {i}")
```

## 5. 列表推导式 (List Comprehension)

### 5.1 基本语法
```python
# 传统方式
squares = []
for i in range(5):
    squares.append(i ** 2)

# 列表推导式
squares = [i ** 2 for i in range(5)]
```

### 5.2 带条件的列表推导式
```python
# 只包含偶数的平方
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
```

## 6. 实际应用示例

### 6.1 成绩统计系统
```python
scores = [85, 92, 78, 96, 88, 76, 94, 89, 91, 87]

# 统计各等级人数
excellent = 0  # 优秀 (90+)
good = 0       # 良好 (80-89)
pass_grade = 0 # 及格 (60-79)
fail = 0       # 不及格 (<60)

for score in scores:
    if score >= 90:
        excellent += 1
    elif score >= 80:
        good += 1
    elif score >= 60:
        pass_grade += 1
    else:
        fail += 1

print(f"优秀: {excellent}人")
print(f"良好: {good}人")
print(f"及格: {pass_grade}人")
print(f"不及格: {fail}人")
```

### 6.2 猜数字游戏
```python
import random

secret_number = random.randint(1, 100)
attempts = 0
max_attempts = 7

print("猜数字游戏！我想了一个1到100之间的数字。")

while attempts < max_attempts:
    guess = int(input("请输入你的猜测: "))
    attempts += 1
    
    if guess == secret_number:
        print(f"恭喜！你猜对了！用了{attempts}次。")
        break
    elif guess < secret_number:
        print("太小了！")
    else:
        print("太大了！")
else:
    print(f"游戏结束！正确答案是{secret_number}。")
```

### 6.3 查找最大最小值
```python
numbers = [45, 23, 78, 12, 67, 89, 34, 56]

# 查找最大值
max_value = numbers[0]
for num in numbers:
    if num > max_value:
        max_value = num

# 查找最小值
min_value = numbers[0]
for num in numbers:
    if num < min_value:
        min_value = num

print(f"最大值: {max_value}")
print(f"最小值: {min_value}")
```

## 7. 常见错误与注意事项

### 7.1 缩进错误
```python
# ❌ 错误：缩进不一致
if True:
    print("正确")
  print("错误")  # 缩进错误

# ✅ 正确：使用4个空格或1个Tab
if True:
    print("正确")
    print("正确")
```

### 7.2 无限循环
```python
# ❌ 危险：可能造成无限循环
count = 0
while count < 10:
    print(count)
    # 忘记增加 count，导致无限循环

# ✅ 正确：确保循环条件会改变
count = 0
while count < 10:
    print(count)
    count += 1
```

### 7.3 变量作用域
```python
# 在循环中定义的变量在循环外也可以访问
for i in range(3):
    temp = i * 2

print(temp)  # 可以访问，值为 4
```

## 重要提示

1. **缩进很重要**：Python 使用缩进来表示代码块
2. **条件表达式**：任何非零、非空的值都被视为 True
3. **循环优化**：避免在循环中进行重复计算
4. **可读性**：复杂的嵌套结构要考虑重构
5. **调试技巧**：使用 print() 语句来跟踪程序执行

# 你可以在底下的代码编辑器中，输入你的代码。

![img.png](./assets/01-02/img.png)

# 然后，点击按钮，交由AI评论
