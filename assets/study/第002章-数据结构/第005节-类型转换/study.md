# 类型转换

## 一、什么是类型转换

类型转换是将一种数据类型转换为另一种数据类型的过程。Python提供了内置函数来进行类型转换。

## 二、常用类型转换函数

### 1. int() - 转换为整数

```python
# 字符串转整数
num1 = int("123")
print(num1)  # 输出：123

# 浮点数转整数（截断小数部分）
num2 = int(3.14)
print(num2)  # 输出：3

# 布尔值转整数
num3 = int(True)
num4 = int(False)
print(num3, num4)  # 输出：1 0
```

### 2. float() - 转换为浮点数

```python
# 字符串转浮点数
num1 = float("3.14")
print(num1)  # 输出：3.14

# 整数转浮点数
num2 = float(5)
print(num2)  # 输出：5.0

# 布尔值转浮点数
num3 = float(True)
print(num3)  # 输出：1.0
```

### 3. str() - 转换为字符串

```python
# 数字转字符串
text1 = str(123)
text2 = str(3.14)
print(text1, text2)  # 输出：123 3.14

# 布尔值转字符串
text3 = str(True)
text4 = str(False)
print(text3, text4)  # 输出：True False

# 列表转字符串
text5 = str([1, 2, 3])
print(text5)  # 输出：[1, 2, 3]
```

### 4. bool() - 转换为布尔值

```python
# 数字转布尔值（0为False，非0为True）
print(bool(0))    # 输出：False
print(bool(1))    # 输出：True
print(bool(-5))   # 输出：True

# 字符串转布尔值（空字符串为False，非空为True）
print(bool(""))   # 输出：False
print(bool("hello"))  # 输出：True

# 列表转布尔值（空列表为False，非空为True）
print(bool([]))   # 输出：False
print(bool([1, 2]))  # 输出：True
```

## 三、类型转换的注意事项

### 1. 转换错误

```python
# 不能将非数字字符串转换为整数
# int("hello")  # 会报错

# 不能将非数字字符串转换为浮点数
# float("abc")  # 会报错
```

### 2. 精度丢失

```python
# 浮点数转整数会丢失小数部分
num = int(3.99)
print(num)  # 输出：3（不是4）
```

### 3. 字符串格式

```python
# 字符串必须符合数字格式才能转换
print(int("123"))     # 正确
# print(int("12.3"))  # 错误，不能直接转换带小数点的字符串
print(float("12.3"))  # 正确
```

## 四、实际应用示例

### 1. 用户输入处理

```python
# 用户输入的是字符串，需要转换为数字进行计算
age_str = "25"
age = int(age_str)
next_year = age + 1
print(f"明年你{next_year}岁")
```

### 2. 数据验证

```python
# 检查输入是否为有效数字
user_input = "123"
if user_input.isdigit():
    number = int(user_input)
    print(f"有效数字：{number}")
else:
    print("请输入有效数字")
```

### 3. 类型检查

```python
# 确保数据类型正确
score = 85.5
score_str = str(score)
print(f"成绩：{score_str}分")

# 检查是否为真值
value = 0
if bool(value):
    print("值为真")
else:
    print("值为假")
```

## 五、常见转换场景

```python
# 1. 数学计算中的类型转换
a = "10"
b = "20"
result = int(a) + int(b)
print(result)  # 输出：30

# 2. 字符串拼接中的类型转换
name = "张三"
age = 25
message = name + "今年" + str(age) + "岁"
print(message)  # 输出：张三今年25岁

# 3. 条件判断中的类型转换
user_input = "1"
if int(user_input) == 1:
    print("用户选择了选项1")
```

## 注意事项

- 转换前要确保数据格式正确
- 注意精度丢失问题
- 了解各种类型的真假值判断规则
