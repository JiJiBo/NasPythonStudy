# 📝 Python 列表生成式详解

## 1. 什么是列表生成式

列表生成式（List Comprehension）是 Python 中一种**简洁、优雅的创建列表的方法**。它可以用一行代码代替传统的循环来生成列表，让代码更加简洁和高效。

## 2. 基本语法

### 2.1 基本格式
```python
[表达式 for 变量 in 可迭代对象]
```

### 2.2 简单示例
要生成 list [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]，我们可以用 range(1, 11)：

```python
list(range(1, 11))
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

但如果要生成 [1×1, 2×2, 3×3, ..., 10×10] 怎么做？方法一是循环：

```python
L = []
for x in range(1, 11):
    L.append(x * x)
print(L)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

但是循环太繁琐，而列表生成式则可以用一行语句代替循环生成上面的 list：

```python
[x * x for x in range(1, 11)]
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

这种写法就是 Python 特有的列表生成式。利用列表生成式，可以以非常简洁的代码生成 list。

写列表生成式时，把要生成的元素 `x * x` 放到前面，后面跟 for 循环，就可以把 list 创建出来。

## 3. 条件过滤

列表生成式的 for 循环后面还可以加上 if 判断。例如：

```python
[x * x for x in range(1, 11)]
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

如果我们只想要偶数的平方，不改动 range() 的情况下，可以加上 if 来筛选：

```python
[x * x for x in range(1, 11) if x % 2 == 0]
# [4, 16, 36, 64, 100]
```

有了 if 条件，只有 if 判断为 True 的时候，才把循环的当前元素添加到列表中。

### 3.1 基本条件过滤
```python
# 生成1到20的偶数
even_numbers = [x for x in range(1, 21) if x % 2 == 0]
print(even_numbers)  # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# 生成1到10的奇数
odd_numbers = [x for x in range(1, 11) if x % 2 == 1]
print(odd_numbers)  # [1, 3, 5, 7, 9]
```

### 3.2 复杂条件过滤
```python
# 生成能被3整除且大于10的数字
numbers = [x for x in range(1, 31) if x % 3 == 0 and x > 10]
print(numbers)  # [12, 15, 18, 21, 24, 27, 30]

# 过滤掉空字符串
words = ["hello", "", "world", "", "python"]
non_empty = [word for word in words if word]
print(non_empty)  # ["hello", "world", "python"]
```

## 4. 多重循环

### 4.1 基本多重循环
```python
# 生成所有可能的坐标组合
coordinates = [(x, y) for x in range(3) for y in range(3)]
print(coordinates)
# [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

# 生成乘法表
multiplication_table = [f"{i}×{j}={i*j}" for i in range(1, 4) for j in range(1, 4)]
print(multiplication_table)
# ["1×1=1", "1×2=2", "1×3=3", "2×1=2", "2×2=4", "2×3=6", "3×1=3", "3×2=6", "3×3=9"]
```

### 4.2 带条件的多重循环
```python
# 生成不重复的坐标组合（x != y）
unique_coords = [(x, y) for x in range(3) for y in range(3) if x != y]
print(unique_coords)
# [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
```

## 5. 嵌套列表生成式

### 5.1 基本嵌套
```python
# 生成二维列表
matrix = [[i + j for j in range(3)] for i in range(3)]
print(matrix)
# [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

# 生成三角形数字
triangle = [[j for j in range(i + 1)] for i in range(4)]
print(triangle)
# [[0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
```

### 5.2 扁平化嵌套列表
```python
# 将嵌套列表扁平化
nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for sublist in nested_list for item in sublist]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## 6. 字典和集合生成式

### 6.1 字典生成式
```python
# 创建数字到其平方的映射
squares_dict = {x: x**2 for x in range(1, 6)}
print(squares_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 过滤字典
original_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
filtered_dict = {k: v for k, v in original_dict.items() if v > 2}
print(filtered_dict)  # {"c": 3, "d": 4}
```

### 6.2 集合生成式
```python
# 创建包含平方数的集合
squares_set = {x**2 for x in range(1, 6)}
print(squares_set)  # {1, 4, 9, 16, 25}

# 从字符串中提取唯一字符
text = "hello world"
unique_chars = {char for char in text if char != " "}
print(unique_chars)  # {"h", "e", "l", "o", "w", "r", "d"}
```

## 7. 实际应用示例

### 7.1 数据处理
```python
# 处理学生成绩
scores = [85, 92, 78, 96, 88, 76, 94, 89, 91, 87]

# 找出优秀成绩（>=90）
excellent_scores = [score for score in scores if score >= 90]
print(excellent_scores)  # [92, 96, 94, 91]

# 计算成绩等级
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "D"

grades = [get_grade(score) for score in scores]
print(grades)  # ["B", "A", "C", "A", "B", "C", "A", "B", "A", "B"]
```

### 7.2 文本处理
```python
# 处理文本数据
text = "Python is a great programming language"
words = text.split()

# 获取所有单词的长度
word_lengths = [len(word) for word in words]
print(word_lengths)  # [6, 2, 1, 5, 11, 8]

# 获取长度大于3的单词
long_words = [word for word in words if len(word) > 3]
print(long_words)  # ["Python", "great", "programming", "language"]

# 将单词转换为大写
upper_words = [word.upper() for word in words]
print(upper_words)  # ["PYTHON", "IS", "A", "GREAT", "PROGRAMMING", "LANGUAGE"]
```

### 7.3 文件处理
```python
# 模拟文件内容
file_lines = [
    "apple,red,5",
    "banana,yellow,3",
    "orange,orange,4",
    "grape,purple,2"
]

# 解析CSV数据
parsed_data = [line.split(",") for line in file_lines]
print(parsed_data)
# [["apple", "red", "5"], ["banana", "yellow", "3"], ["orange", "orange", "4"], ["grape", "purple", "2"]]

# 提取水果名称
fruit_names = [item[0] for item in parsed_data]
print(fruit_names)  # ["apple", "banana", "orange", "grape"]
```

## 8. 性能考虑

### 8.1 列表生成式 vs 传统循环
```python
import time

# 大列表
n = 1000000

# 列表生成式（更快）
start_time = time.time()
squares_lc = [x**2 for x in range(n)]
lc_time = time.time() - start_time

# 传统循环（较慢）
start_time = time.time()
squares_loop = []
for x in range(n):
    squares_loop.append(x**2)
loop_time = time.time() - start_time

print(f"列表生成式时间: {lc_time:.6f}秒")
print(f"传统循环时间: {loop_time:.6f}秒")
```

### 8.2 内存效率
```python
# 生成器表达式（内存高效）
squares_gen = (x**2 for x in range(1000000))

# 列表生成式（占用更多内存）
squares_list = [x**2 for x in range(1000000)]

# 使用生成器表达式
for square in squares_gen:
    if square > 100:
        break
    print(square)
```

## 9. 常见错误与注意事项

### 9.1 变量作用域
```python
# ❌ 错误：在列表生成式外部使用循环变量
# squares = [x**2 for x in range(5)]
# print(x)  # NameError: name 'x' is not defined

# ✅ 正确：循环变量只在列表生成式内部有效
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]
```

### 9.2 副作用
```python
# ❌ 避免在列表生成式中使用有副作用的操作
# results = [print(x) for x in range(5)]  # 不推荐

# ✅ 正确：先计算，再处理
numbers = [x for x in range(5)]
for num in numbers:
    print(num)
```

### 9.3 复杂逻辑
```python
# ❌ 避免过于复杂的列表生成式
# complex_result = [x**2 if x % 2 == 0 else x**3 if x > 5 else x for x in range(10) if x != 3]

# ✅ 正确：使用函数处理复杂逻辑
def process_number(x):
    if x == 3:
        return None
    if x % 2 == 0:
        return x**2
    elif x > 5:
        return x**3
    else:
        return x

simple_result = [process_number(x) for x in range(10) if process_number(x) is not None]
```

## 10. 高级技巧

### 10.1 条件表达式
```python
# 使用三元运算符
numbers = [1, 2, 3, 4, 5]
result = ["偶数" if x % 2 == 0 else "奇数" for x in numbers]
print(result)  # ["奇数", "偶数", "奇数", "偶数", "奇数"]
```

### 10.2 函数调用
```python
# 在列表生成式中调用函数
def square(x):
    return x**2

def is_even(x):
    return x % 2 == 0

squares = [square(x) for x in range(1, 6) if is_even(x)]
print(squares)  # [4, 16]
```

### 10.3 嵌套条件
```python
# 多重条件
numbers = range(1, 21)
result = [x for x in numbers if x % 2 == 0 if x % 3 == 0]
print(result)  # [6, 12, 18]

# 等价于
result2 = [x for x in numbers if x % 2 == 0 and x % 3 == 0]
print(result2)  # [6, 12, 18]
```

## 重要提示

1. **简洁性**：列表生成式让代码更简洁、可读性更强
2. **性能**：通常比传统循环更快
3. **条件过滤**：使用 if 条件进行过滤
4. **多重循环**：支持嵌套循环
5. **类型多样**：支持列表、字典、集合生成式
6. **避免复杂**：过于复杂的逻辑应该使用函数

# 你可以在底下的代码编辑器中，输入你的代码。

![img.png](./assets/01-02/img.png)

# 然后，点击按钮，交由AI评论
