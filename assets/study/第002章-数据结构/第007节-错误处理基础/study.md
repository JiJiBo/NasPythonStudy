# 错误处理基础

## 一、什么是错误

在编程过程中，程序可能会遇到各种问题，这些问题会导致程序无法正常运行，这就是错误。

## 二、常见错误类型

### 1. 语法错误（SyntaxError）

代码语法不正确：

```python
# 缺少冒号
if x > 5
    print("x大于5")

# 缺少括号
print("Hello World"

# 缩进错误
if x > 5:
print("x大于5")
```

### 2. 名称错误（NameError）

使用了未定义的变量：

```python
# 变量未定义
print(undefined_variable)

# 函数名拼写错误
prnt("Hello")  # 应该是 print
```

### 3. 类型错误（TypeError）

对不支持的操作使用了错误的数据类型：

```python
# 字符串和数字相加
result = "Hello" + 123

# 对字符串使用数学运算
result = "abc" * "def"
```

### 4. 值错误（ValueError）

函数接收到了正确类型但值不合适的参数：

```python
# 字符串转数字时包含非数字字符
num = int("abc")

# 列表索引超出范围
numbers = [1, 2, 3]
print(numbers[10])
```

### 5. 索引错误（IndexError）

访问列表或字符串时索引超出范围：

```python
# 列表索引超出范围
numbers = [1, 2, 3]
print(numbers[5])

# 字符串索引超出范围
text = "Hello"
print(text[10])
```

## 三、如何阅读错误信息

Python的错误信息包含以下信息：

```python
Traceback (most recent call last):
  File "example.py", line 5, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero
```

- **Traceback**：错误发生的位置
- **File "example.py"**：文件名
- **line 5**：错误发生的行号
- **ZeroDivisionError**：错误类型
- **division by zero**：错误描述

## 四、基本错误处理

### 1. 使用 try-except 语句

```python
try:
    # 可能出错的代码
    num = int(input("请输入一个数字："))
    result = 10 / num
    print(f"结果是：{result}")
except ValueError:
    # 处理值错误
    print("请输入有效的数字！")
except ZeroDivisionError:
    # 处理除零错误
    print("不能除以零！")
except Exception as e:
    # 处理其他所有错误
    print(f"发生错误：{e}")
```

### 2. 处理多种错误

```python
try:
    age = int(input("请输入年龄："))
    if age < 0:
        raise ValueError("年龄不能为负数")
    print(f"你的年龄是：{age}")
except ValueError as e:
    print(f"输入错误：{e}")
```

### 3. 使用 else 和 finally

```python
try:
    num = int(input("请输入数字："))
    result = 10 / num
except ValueError:
    print("请输入有效数字！")
except ZeroDivisionError:
    print("不能除以零！")
else:
    # 如果没有错误，执行这里
    print(f"计算成功：{result}")
finally:
    # 无论是否有错误，都会执行这里
    print("程序结束")
```

## 五、实际应用示例

### 1. 安全的用户输入

```python
def get_safe_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("请输入有效的数字！")

# 使用安全输入函数
age = get_safe_number("请输入年龄：")
height = get_safe_number("请输入身高（米）：")
print(f"年龄：{age}，身高：{height}米")
```

### 2. 文件操作错误处理

```python
try:
    with open("nonexistent_file.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("文件不存在！")
except PermissionError:
    print("没有权限读取文件！")
```

### 3. 列表操作错误处理

```python
def safe_get_item(lst, index):
    try:
        return lst[index]
    except IndexError:
        print(f"索引 {index} 超出范围，列表长度为 {len(lst)}")
        return None

# 使用安全获取函数
numbers = [1, 2, 3, 4, 5]
result1 = safe_get_item(numbers, 2)  # 正常
result2 = safe_get_item(numbers, 10)  # 错误
```

## 六、调试技巧

### 1. 使用 print 调试

```python
x = 10
y = 0
print(f"x = {x}, y = {y}")  # 调试信息

try:
    result = x / y
    print(f"结果：{result}")
except ZeroDivisionError:
    print("除零错误！")
```

### 2. 检查变量值

```python
user_input = input("请输入数字：")
print(f"用户输入：'{user_input}'")  # 检查输入内容

try:
    num = int(user_input)
    print(f"转换后：{num}")
except ValueError:
    print("转换失败")
```

## 七、预防错误的建议

### 1. 输入验证

```python
# 检查输入是否为空
user_input = input("请输入姓名：")
if not user_input.strip():
    print("姓名不能为空！")
else:
    print(f"你好，{user_input}！")
```

### 2. 类型检查

```python
# 检查变量类型
value = input("请输入数字：")
if value.isdigit():
    num = int(value)
    print(f"有效数字：{num}")
else:
    print("请输入数字！")
```

### 3. 范围检查

```python
# 检查数值范围
age = int(input("请输入年龄："))
if 0 <= age <= 150:
    print(f"年龄：{age}")
else:
    print("年龄必须在0-150之间！")
```

## 注意事项

- 总是处理可能的错误情况
- 使用具体的错误类型而不是通用的Exception
- 提供有意义的错误信息
- 在开发阶段使用详细的错误信息，生产环境可以简化
- 不要忽略错误，至少要记录日志
