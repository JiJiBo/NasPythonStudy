# 🔧 Python 函数详解

## 1. 什么是函数

函数是一段**可重复使用的代码块**，它接受输入参数，执行特定任务，并返回结果。函数让代码更加模块化、可读性更强。

## 2. 函数的定义

### 2.1 基本语法
```python
def 函数名(参数1, 参数2, ...):
    """函数文档字符串"""
    函数体
    return 返回值  # 可选
```

### 2.2 简单示例
```python
def greet():
    """简单的问候函数"""
    print("Hello, World!")

# 调用函数
greet()  # 输出: Hello, World!
```

### 2.3 带参数的函数
```python
def greet(name):
    """带参数的问候函数"""
    print(f"Hello, {name}!")

greet("张三")  # 输出: Hello, 张三!
```

## 3. 函数参数

### 3.1 位置参数
```python
def add(a, b):
    """加法函数"""
    return a + b

result = add(3, 5)  # a=3, b=5
print(result)  # 8
```

### 3.2 默认参数
```python
def greet(name, greeting="Hello"):
    """带默认参数的问候函数"""
    print(f"{greeting}, {name}!")

greet("李四")           # Hello, 李四!
greet("王五", "Hi")     # Hi, 王五!
```

### 3.3 关键字参数
```python
def create_profile(name, age, city="北京", job="学生"):
    """创建用户档案"""
    return {
        "name": name,
        "age": age,
        "city": city,
        "job": job
    }

# 使用关键字参数
profile = create_profile(name="赵六", age=25, job="程序员")
print(profile)
```

### 3.4 可变参数
```python
def sum_all(*numbers):
    """计算所有数字的和"""
    total = 0
    for num in numbers:
        total += num
    return total

result1 = sum_all(1, 2, 3)        # 6
result2 = sum_all(1, 2, 3, 4, 5)  # 15
```

### 3.5 关键字可变参数
```python
def create_student(**info):
    """创建学生信息"""
    student = {}
    for key, value in info.items():
        student[key] = value
    return student

student = create_student(name="小明", age=20, grade="A", major="计算机")
print(student)
```

## 4. 返回值

### 4.1 单个返回值
```python
def square(x):
    """计算平方"""
    return x * x

result = square(5)  # 25
```

### 4.2 多个返回值
```python
def get_name_and_age():
    """返回姓名和年龄"""
    return "张三", 25

name, age = get_name_and_age()
print(f"姓名: {name}, 年龄: {age}")
```

### 4.3 无返回值
```python
def print_info(name, age):
    """打印信息，无返回值"""
    print(f"姓名: {name}, 年龄: {age}")

result = print_info("李四", 30)  # 输出信息
print(result)  # None
```

## 5. 函数的作用域

### 5.1 局部变量
```python
def my_function():
    local_var = "我是局部变量"
    print(local_var)

my_function()
# print(local_var)  # 错误！局部变量在函数外不可访问
```

### 5.2 全局变量
```python
global_var = "我是全局变量"

def my_function():
    print(global_var)  # 可以访问全局变量

my_function()
```

### 5.3 global 关键字
```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
print(counter)  # 1
```

## 6. 函数的高级特性

### 6.1 嵌套函数
```python
def outer_function(x):
    """外部函数"""
    def inner_function(y):
        """内部函数"""
        return x + y
    return inner_function

add_five = outer_function(5)
result = add_five(3)  # 8
```

### 6.2 闭包
```python
def create_multiplier(n):
    """创建乘法器"""
    def multiplier(x):
        return x * n
    return multiplier

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

### 6.3 装饰器
```python
def my_decorator(func):
    """装饰器函数"""
    def wrapper(*args, **kwargs):
        print("函数执行前")
        result = func(*args, **kwargs)
        print("函数执行后")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("世界")
```

## 7. Lambda 函数

### 7.1 基本语法
```python
# 普通函数
def square(x):
    return x * x

# Lambda 函数
square_lambda = lambda x: x * x

print(square(5))        # 25
print(square_lambda(5)) # 25
```

### 7.2 与内置函数结合
```python
# 使用 map
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

# 使用 filter
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4]

# 使用 sorted
students = [("张三", 85), ("李四", 92), ("王五", 78)]
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
print(sorted_students)  # [("李四", 92), ("张三", 85), ("王五", 78)]
```

## 8. 递归函数

### 8.1 基本递归
```python
def factorial(n):
    """计算阶乘"""
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(5))  # 120
```

### 8.2 斐波那契数列
```python
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(10):
    print(fibonacci(i), end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

## 9. 实际应用示例

### 9.1 计算器函数
```python
def calculator(operation, a, b):
    """简单计算器"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b != 0:
            return a / b
        else:
            return "错误：除数不能为零"
    else:
        return "错误：不支持的操作"

print(calculator("add", 10, 5))      # 15
print(calculator("divide", 10, 0))   # 错误：除数不能为零
```

### 9.2 数据验证函数
```python
def validate_email(email):
    """验证邮箱格式"""
    if "@" in email and "." in email:
        return True
    return False

def validate_age(age):
    """验证年龄"""
    if isinstance(age, int) and 0 <= age <= 150:
        return True
    return False

# 测试
emails = ["test@example.com", "invalid-email", "user@domain.org"]
for email in emails:
    print(f"{email}: {validate_email(email)}")
```

### 9.3 文件处理函数
```python
def read_file_lines(filename):
    """读取文件的所有行"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        return f"文件 {filename} 不存在"
    except Exception as e:
        return f"读取文件时出错: {e}"

def write_to_file(filename, content):
    """写入内容到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return "写入成功"
    except Exception as e:
        return f"写入文件时出错: {e}"
```

## 10. 函数的最佳实践

### 10.1 函数命名
```python
# ✅ 好的命名
def calculate_average_score(scores):
    pass

def get_user_by_id(user_id):
    pass

# ❌ 不好的命名
def func1():
    pass

def calc():
    pass
```

### 10.2 文档字符串
```python
def calculate_rectangle_area(length, width):
    """
    计算矩形的面积
    
    参数:
        length (float): 矩形的长度
        width (float): 矩形的宽度
    
    返回:
        float: 矩形的面积
    
    示例:
        >>> calculate_rectangle_area(5, 3)
        15.0
    """
    return length * width
```

### 10.3 错误处理
```python
def safe_divide(a, b):
    """安全的除法运算"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "错误：除数不能为零"
    except TypeError:
        return "错误：参数类型不正确"
    except Exception as e:
        return f"未知错误: {e}"
```

## 11. 常见错误与注意事项

### 11.1 可变默认参数
```python
# ❌ 错误：可变默认参数
def add_item(item, my_list=[]):
    my_list.append(item)
    return my_list

# ✅ 正确：使用 None 作为默认值
def add_item(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

### 11.2 变量作用域混淆
```python
# ❌ 错误：试图修改全局变量
x = 10

def modify_x():
    x = 20  # 这创建了一个新的局部变量

modify_x()
print(x)  # 仍然是 10

# ✅ 正确：使用 global 关键字
def modify_x():
    global x
    x = 20

modify_x()
print(x)  # 现在是 20
```

## 重要提示

1. **函数名要有意义**：使用动词或动词短语
2. **参数要合理**：避免参数过多，考虑使用字典或对象
3. **返回值要明确**：要么有明确的返回值，要么明确返回 None
4. **文档要完整**：为函数编写清晰的文档字符串
5. **错误要处理**：适当处理可能的异常情况
6. **测试要充分**：为函数编写测试用例

# 你可以在底下的代码编辑器中，输入你的代码。

![img.png](./assets/01-02/img.png)

# 然后，点击按钮，交由AI评论
