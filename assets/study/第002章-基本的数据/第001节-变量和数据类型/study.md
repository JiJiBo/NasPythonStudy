# 🐍 Python 基本数据类型详解

## 1. 什么是数据类型

在 Python 中，**数据类型**决定了变量可以存储什么样的数据以及能对这些数据执行什么操作。

## 2. Python 的基本数据类型

### 2.1 数字类型 (Numbers)

#### 整数 (int)
```python
age = 25
score = 100
temperature = -10
```

#### 浮点数 (float)
```python
height = 1.75
pi = 3.14159
price = 99.99
```

#### 复数 (complex)
```python
z = 3 + 4j
```

### 2.2 字符串类型 (str)
```python
name = "张三"
message = 'Hello World'
address = """北京市
朝阳区
三里屯"""
```

### 2.3 布尔类型 (bool)
```python
is_student = True
is_working = False
```

### 2.4 空值类型 (NoneType)
```python
result = None
```

## 3. 类型检查

使用 `type()` 函数查看变量的数据类型：

```python
age = 25
print(type(age))        # <class 'int'>
print(type(25.5))       # <class 'float'>
print(type("Hello"))    # <class 'str'>
print(type(True))       # <class 'bool'>
print(type(None))       # <class 'NoneType'>
```

## 4. 类型转换

### 4.1 隐式类型转换
```python
# 整数和浮点数运算，结果自动转为浮点数
result = 5 + 3.14  # 8.14 (float)
```

### 4.2 显式类型转换
```python
# 转换为整数
age_str = "25"
age_int = int(age_str)

# 转换为浮点数
score_str = "98.5"
score_float = float(score_str)

# 转换为字符串
age = 25
age_str = str(age)

# 转换为布尔值
print(bool(1))      # True
print(bool(0))      # False
print(bool(""))     # False
print(bool("abc"))  # True
```

## 5. 变量赋值与多重赋值

### 5.1 单个赋值
```python
name = "李四"
age = 20
```

### 5.2 多重赋值
```python
# 同时给多个变量赋值
x, y, z = 1, 2, 3

# 给多个变量赋相同值
a = b = c = 0
```

## 6. 变量的作用域

### 6.1 局部变量
```python
def my_function():
    local_var = "我是局部变量"
    print(local_var)

my_function()
# print(local_var)  # 错误！局部变量在函数外不可访问
```

### 6.2 全局变量
```python
global_var = "我是全局变量"

def my_function():
    print(global_var)  # 可以访问全局变量

my_function()
print(global_var)  # 也可以访问
```

## 7. 常量

Python 没有真正的常量，但约定用全大写字母表示常量：

```python
PI = 3.14159
MAX_SIZE = 100
DEFAULT_NAME = "Unknown"
```

## 8. 内存管理

### 8.1 引用计数
```python
a = [1, 2, 3]
b = a  # b 和 a 指向同一个对象
print(id(a))  # 查看对象的内存地址
print(id(b))  # 相同的内存地址
```

### 8.2 垃圾回收
```python
a = [1, 2, 3]
a = None  # 原来的列表对象会被垃圾回收
```

## 9. 数据类型的特点

### 9.1 可变类型 vs 不可变类型

**不可变类型**：int, float, str, bool, tuple
```python
x = 10
x = 20  # 创建新的整数对象，不是修改原来的
```

**可变类型**：list, dict, set
```python
my_list = [1, 2, 3]
my_list.append(4)  # 修改原来的列表对象
```

## 10. 实际应用示例

```python
# 学生信息管理系统
student_name = "王小明"      # 字符串
student_age = 18            # 整数
student_height = 1.75       # 浮点数
is_graduated = False        # 布尔值
subjects = None             # 空值

# 类型检查
print(f"姓名: {student_name}, 类型: {type(student_name)}")
print(f"年龄: {student_age}, 类型: {type(student_age)}")
print(f"身高: {student_height}, 类型: {type(student_height)}")
print(f"是否毕业: {is_graduated}, 类型: {type(is_graduated)}")
```

## 重要提示

1. **动态类型**：Python 是动态类型语言，变量类型可以在运行时改变
2. **强类型**：Python 是强类型语言，不同类型间的运算需要显式转换
3. **内存效率**：了解数据类型有助于编写更高效的代码
4. **调试技巧**：使用 `type()` 和 `isinstance()` 来检查变量类型

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
