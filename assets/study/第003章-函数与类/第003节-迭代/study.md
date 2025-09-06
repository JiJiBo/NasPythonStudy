# 🔄 Python 迭代详解

## 1. 什么是迭代

在 Python 中，如果给定一个 list 或 tuple，我们可以通过 for 循环来遍历这个 list 或 tuple，这种遍历我们称为**迭代（Iteration）**。

Python 的 for 循环不仅可以用在 list 或 tuple 上，还可以作用在其他任何可迭代对象上。

因此，迭代操作就是对于一个集合，无论该集合是有序还是无序，我们用 for 循环总是可以依次取出集合的每一个元素。

```
注意: 集合是指包含一组元素的数据结构，我们已经介绍的包括：
1. 有序集合：list，tuple，str 和 unicode；
2. 无序集合：set
3. 无序集合并且具有 key-value 对：dict
```

而迭代是一个动词，它指的是一种操作，在 Python 中，就是 for 循环。

迭代与按下标访问数组最大的不同是，后者是一种具体的迭代实现方式，而前者只关心迭代结果，根本不关心迭代内部是如何实现的。

## 2. 基本迭代操作

### 2.1 列表迭代
```python
fruits = ["苹果", "香蕉", "橙子", "葡萄"]

# 基本迭代
for fruit in fruits:
    print(fruit)

# 输出：
# 苹果
# 香蕉
# 橙子
# 葡萄
```

### 2.2 字符串迭代
```python
text = "Python"

for char in text:
    print(char)

# 输出：
# P
# y
# t
# h
# o
# n
```

### 2.3 元组迭代
```python
coordinates = (10, 20, 30)

for coord in coordinates:
    print(coord)

# 输出：
# 10
# 20
# 30
```

### 2.4 集合迭代
```python
unique_numbers = {1, 3, 5, 7, 9}

for num in unique_numbers:
    print(num)

# 输出（顺序可能不同）：
# 1
# 3
# 5
# 7
# 9
```

## 3. 索引迭代

Python 中，迭代永远是取出元素本身，而非元素的索引。

对于有序集合，元素确实是有索引的。有的时候，我们确实想在 for 循环中拿到索引，怎么办？

方法是使用 `enumerate()` 函数：

```python
L = ['Adam', 'Lisa', 'Bart', 'Paul']
for index, name in enumerate(L):
    print(f"{index} - {name}")

# 输出：
# 0 - Adam
# 1 - Lisa
# 2 - Bart
# 3 - Paul
```

使用 `enumerate()` 函数，我们可以在 for 循环中同时绑定索引 index 和元素 name。但是，这不是 `enumerate()` 的特殊语法。实际上，`enumerate()` 函数把：

```python
['Adam', 'Lisa', 'Bart', 'Paul']
```

变成了类似：

```python
[(0, 'Adam'), (1, 'Lisa'), (2, 'Bart'), (3, 'Paul')]
```

可见，索引迭代也不是真的按索引访问，而是由 `enumerate()` 函数自动把每个元素变成 `(index, element)` 这样的 tuple，再迭代，就同时获得了索引和元素本身。

### 3.1 enumerate() 的高级用法
```python
# 指定起始索引
fruits = ["苹果", "香蕉", "橙子"]
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")

# 输出：
# 1. 苹果
# 2. 香蕉
# 3. 橙子
```

### 3.2 只获取索引
```python
fruits = ["苹果", "香蕉", "橙子"]
for index in range(len(fruits)):
    print(f"索引 {index}: {fruits[index]}")

# 输出：
# 索引 0: 苹果
# 索引 1: 香蕉
# 索引 2: 橙子
```

## 4. 迭代字典

### 4.1 迭代字典的键
```python
student_scores = {"张三": 85, "李四": 92, "王五": 78}

# 默认迭代键
for name in student_scores:
    print(name)

# 或者显式使用 keys()
for name in student_scores.keys():
    print(name)

# 输出：
# 张三
# 李四
# 王五
```

### 4.2 迭代字典的值
通过 `dict.values()` 获取：

```python
student_scores = {"张三": 85, "李四": 92, "王五": 78}

for score in student_scores.values():
    print(score)

# 输出：
# 85
# 92
# 78
```

`values()` 方法实际上把一个 dict 转换成了包含 value 的 list。

### 4.3 迭代字典的键和值
通过 `.items()` 方法，类比 list 的 `enumerate()` 方法，可以直接获取 key 和 value：

```python
d = {"Adam": 95, "Lisa": 85, "Bart": 59}

for key, value in d.items():
    print(f"{key}: {value}")

# 输出：
# Adam: 95
# Lisa: 85
# Bart: 59
```

## 5. 高级迭代技巧

### 5.1 反向迭代
```python
numbers = [1, 2, 3, 4, 5]

# 使用 reversed() 函数
for num in reversed(numbers):
    print(num)

# 输出：
# 5
# 4
# 3
# 2
# 1
```

### 5.2 同时迭代多个序列
```python
names = ["张三", "李四", "王五"]
ages = [20, 25, 30]
scores = [85, 92, 78]

# 使用 zip() 函数
for name, age, score in zip(names, ages, scores):
    print(f"{name}: {age}岁, 成绩{score}分")

# 输出：
# 张三: 20岁, 成绩85分
# 李四: 25岁, 成绩92分
# 王五: 30岁, 成绩78分
```

### 5.3 条件迭代
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 只迭代偶数
for num in numbers:
    if num % 2 == 0:
        print(num)

# 输出：
# 2
# 4
# 6
# 8
# 10
```

## 6. 迭代器对象

### 6.1 什么是迭代器
迭代器是一个实现了迭代器协议的对象，它必须实现 `__iter__()` 和 `__next__()` 方法。

```python
# 创建自定义迭代器
class NumberIterator:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.end:
            num = self.current
            self.current += 1
            return num
        else:
            raise StopIteration

# 使用自定义迭代器
for num in NumberIterator(1, 5):
    print(num)

# 输出：
# 1
# 2
# 3
# 4
```

### 6.2 生成器（Generator）
生成器是一种特殊的迭代器，使用 `yield` 关键字创建：

```python
def number_generator(start, end):
    current = start
    while current < end:
        yield current
        current += 1

# 使用生成器
for num in number_generator(1, 5):
    print(num)

# 输出：
# 1
# 2
# 3
# 4
```

## 7. 实际应用示例

### 7.1 数据统计
```python
scores = [85, 92, 78, 96, 88, 76, 94, 89, 91, 87]

# 计算统计信息
total = 0
count = 0
max_score = 0
min_score = 100

for score in scores:
    total += score
    count += 1
    if score > max_score:
        max_score = score
    if score < min_score:
        min_score = score

average = total / count
print(f"总分: {total}")
print(f"平均分: {average:.2f}")
print(f"最高分: {max_score}")
print(f"最低分: {min_score}")
```

### 7.2 文本处理
```python
text = "Python is a great programming language"
words = text.split()

# 统计单词长度
word_lengths = {}
for word in words:
    length = len(word)
    if length in word_lengths:
        word_lengths[length] += 1
    else:
        word_lengths[length] = 1

print("单词长度统计:")
for length, count in word_lengths.items():
    print(f"长度 {length}: {count} 个单词")
```

### 7.3 文件处理
```python
# 模拟文件内容
file_lines = [
    "第一行内容",
    "第二行内容",
    "第三行内容",
    "第四行内容"
]

# 处理文件行
for line_num, line in enumerate(file_lines, start=1):
    print(f"第 {line_num} 行: {line.strip()}")
```

## 8. 迭代的性能考虑

### 8.1 内存效率
```python
# 列表推导式（创建新列表）
squares_list = [x**2 for x in range(1000000)]

# 生成器表达式（内存高效）
squares_gen = (x**2 for x in range(1000000))

# 使用生成器表达式
for square in squares_gen:
    if square > 100:
        break
    print(square)
```

### 8.2 提前终止迭代
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 找到第一个大于5的数字
for num in numbers:
    if num > 5:
        print(f"找到第一个大于5的数字: {num}")
        break
```

## 9. 常见错误与注意事项

### 9.1 在迭代过程中修改集合
```python
# ❌ 错误：在迭代过程中修改列表
numbers = [1, 2, 3, 4, 5]
# for num in numbers:
#     if num % 2 == 0:
#         numbers.remove(num)  # 这会导致意外行为

# ✅ 正确：创建新列表或使用切片
numbers = [1, 2, 3, 4, 5]
even_numbers = [num for num in numbers if num % 2 == 0]
print(even_numbers)  # [2, 4]
```

### 9.2 迭代器耗尽
```python
# 生成器只能迭代一次
squares = (x**2 for x in range(5))

# 第一次迭代
for square in squares:
    print(square)

# 第二次迭代（不会输出任何内容）
for square in squares:
    print(square)  # 不会执行
```

### 9.3 无限迭代
```python
# ❌ 错误：可能导致无限循环
# numbers = [1, 2, 3]
# for num in numbers:
#     numbers.append(num * 2)  # 无限循环

# ✅ 正确：使用计数器或条件
numbers = [1, 2, 3]
count = 0
for num in numbers:
    if count < 10:  # 限制迭代次数
        print(num)
        count += 1
    else:
        break
```

## 重要提示

1. **迭代是抽象操作**：不关心内部实现，只关心结果
2. **enumerate() 获取索引**：同时获得索引和元素
3. **字典迭代**：使用 keys()、values()、items() 方法
4. **生成器高效**：适合处理大量数据
5. **避免修改集合**：在迭代过程中不要修改正在迭代的集合
6. **使用 break 和 continue**：控制迭代流程

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
