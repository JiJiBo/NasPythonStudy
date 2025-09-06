# 📋 Python List 和 Tuple 详解

## 1. 列表 (List) - 可变序列

### 1.1 什么是列表
列表是 Python 中最常用的数据类型之一，它是一个**有序的、可变的**元素集合。

### 1.2 创建列表
```python
# 空列表
empty_list = []
empty_list2 = list()

# 包含元素的列表
numbers = [1, 2, 3, 4, 5]
fruits = ["苹果", "香蕉", "橙子"]
mixed = [1, "hello", 3.14, True]

# 使用 list() 函数
numbers_from_range = list(range(1, 6))  # [1, 2, 3, 4, 5]
```

### 1.3 访问列表元素
```python
fruits = ["苹果", "香蕉", "橙子", "葡萄", "草莓"]

# 通过索引访问（从0开始）
print(fruits[0])    # 苹果
print(fruits[1])    # 香蕉
print(fruits[-1])   # 草莓（最后一个元素）
print(fruits[-2])   # 葡萄（倒数第二个）

# 切片访问
print(fruits[1:3])  # ['香蕉', '橙子']
print(fruits[:3])   # ['苹果', '香蕉', '橙子']
print(fruits[2:])   # ['橙子', '葡萄', '草莓']
```

### 1.4 修改列表元素
```python
fruits = ["苹果", "香蕉", "橙子"]
fruits[1] = "梨"  # 修改第二个元素
print(fruits)     # ['苹果', '梨', '橙子']

# 批量修改
fruits[0:2] = ["西瓜", "桃子"]
print(fruits)     # ['西瓜', '桃子', '橙子']
```

### 1.5 列表常用方法

#### 添加元素
```python
fruits = ["苹果", "香蕉"]

# append() - 在末尾添加一个元素
fruits.append("橙子")
print(fruits)  # ['苹果', '香蕉', '橙子']

# insert() - 在指定位置插入元素
fruits.insert(1, "葡萄")
print(fruits)  # ['苹果', '葡萄', '香蕉', '橙子']

# extend() - 添加多个元素
fruits.extend(["草莓", "樱桃"])
print(fruits)  # ['苹果', '葡萄', '香蕉', '橙子', '草莓', '樱桃']
```

#### 删除元素
```python
fruits = ["苹果", "香蕉", "橙子", "香蕉"]

# remove() - 删除第一个匹配的元素
fruits.remove("香蕉")
print(fruits)  # ['苹果', '橙子', '香蕉']

# pop() - 删除并返回指定位置的元素
removed = fruits.pop(1)
print(removed)  # 橙子
print(fruits)   # ['苹果', '香蕉']

# del 语句
del fruits[0]
print(fruits)   # ['香蕉']

# clear() - 清空列表
fruits.clear()
print(fruits)   # []
```

#### 查找和统计
```python
numbers = [1, 2, 3, 2, 4, 2, 5]

# index() - 查找元素第一次出现的位置
position = numbers.index(2)
print(position)  # 1

# count() - 统计元素出现次数
count = numbers.count(2)
print(count)  # 3

# in 操作符 - 检查元素是否存在
print(3 in numbers)  # True
print(6 in numbers)  # False
```

#### 排序和反转
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# sort() - 原地排序
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# sort(reverse=True) - 降序排序
numbers.sort(reverse=True)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]

# reverse() - 反转列表
numbers.reverse()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# sorted() - 返回新的排序列表（不修改原列表）
original = [3, 1, 4, 1, 5]
sorted_list = sorted(original)
print(original)   # [3, 1, 4, 1, 5] (原列表不变)
print(sorted_list) # [1, 1, 3, 4, 5]
```

### 1.6 列表推导式
```python
# 基本语法：[表达式 for 变量 in 序列]
squares = [x**2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# 带条件的列表推导式
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# 嵌套列表推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## 2. 元组 (Tuple) - 不可变序列

### 2.1 什么是元组
元组是**有序的、不可变的**元素集合，一旦创建就不能修改。

### 2.2 创建元组
```python
# 空元组
empty_tuple = ()
empty_tuple2 = tuple()

# 包含元素的元组
coordinates = (10, 20)
colors = ("红色", "绿色", "蓝色")
mixed = (1, "hello", 3.14, True)

# 单元素元组（注意逗号）
single = (42,)  # 必须有逗号
not_tuple = (42)  # 这不是元组，是整数

# 使用 tuple() 函数
numbers_tuple = tuple([1, 2, 3, 4, 5])
```

### 2.3 访问元组元素
```python
colors = ("红色", "绿色", "蓝色", "黄色", "紫色")

# 通过索引访问
print(colors[0])    # 红色
print(colors[-1])   # 紫色

# 切片访问
print(colors[1:3])  # ('绿色', '蓝色')
print(colors[:2])   # ('红色', '绿色')
```

### 2.4 元组的特点
```python
# 元组是不可变的
colors = ("红色", "绿色", "蓝色")
# colors[0] = "黑色"  # 错误！不能修改元组元素

# 但可以重新赋值整个元组
colors = ("黑色", "白色", "灰色")
print(colors)  # ('黑色', '白色', '灰色')
```

### 2.5 元组常用方法
```python
numbers = (1, 2, 3, 2, 4, 2, 5)

# index() - 查找元素第一次出现的位置
position = numbers.index(2)
print(position)  # 1

# count() - 统计元素出现次数
count = numbers.count(2)
print(count)  # 3

# len() - 获取元组长度
print(len(numbers))  # 7
```

### 2.6 元组解包
```python
# 基本解包
coordinates = (10, 20)
x, y = coordinates
print(f"x = {x}, y = {y}")  # x = 10, y = 20

# 多重赋值
a, b, c = 1, 2, 3
print(f"a = {a}, b = {b}, c = {c}")  # a = 1, b = 2, c = 3

# 使用 * 收集剩余元素
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
print(f"first = {first}")    # first = 1
print(f"middle = {middle}")  # middle = [2, 3, 4]
print(f"last = {last}")      # last = 5
```

## 3. 列表 vs 元组

### 3.1 主要区别
| 特性 | 列表 (List) | 元组 (Tuple) |
|------|-------------|--------------|
| 可变性 | 可变 | 不可变 |
| 语法 | `[1, 2, 3]` | `(1, 2, 3)` |
| 方法 | 丰富的方法 | 有限的方法 |
| 性能 | 稍慢 | 更快 |
| 内存 | 占用更多 | 占用更少 |

### 3.2 使用场景
```python
# 列表适用于需要修改的场景
shopping_cart = ["苹果", "香蕉"]
shopping_cart.append("橙子")  # 可以修改

# 元组适用于不需要修改的场景
coordinates = (10, 20)  # 坐标通常不会改变
colors = ("红色", "绿色", "蓝色")  # 固定的颜色集合
```

## 4. 嵌套结构

### 4.1 嵌套列表
```python
# 二维列表（矩阵）
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 访问元素
print(matrix[0][1])  # 2
print(matrix[2][2])  # 9

# 修改元素
matrix[1][1] = 10
print(matrix[1])  # [4, 10, 6]
```

### 4.2 列表和元组混合
```python
# 列表中包含元组
students = [
    ("张三", 20, "计算机"),
    ("李四", 19, "数学"),
    ("王五", 21, "物理")
]

# 元组中包含列表
config = (
    "数据库配置",
    ["localhost", "user", "password"],
    {"port": 3306, "charset": "utf8"}
)
```

## 5. 实际应用示例

### 5.1 学生成绩管理系统
```python
# 使用列表存储学生信息
students = [
    {"name": "张三", "scores": [85, 92, 78]},
    {"name": "李四", "scores": [90, 88, 95]},
    {"name": "王五", "scores": [76, 84, 89]}
]

# 计算每个学生的平均分
for student in students:
    name = student["name"]
    scores = student["scores"]
    average = sum(scores) / len(scores)
    print(f"{name}的平均分: {average:.2f}")
```

### 5.2 坐标系统
```python
# 使用元组表示坐标
points = [(0, 0), (1, 1), (2, 4), (3, 9)]

# 计算两点之间的距离
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# 计算相邻点之间的距离
for i in range(len(points) - 1):
    dist = distance(points[i], points[i + 1])
    print(f"点{points[i]}到点{points[i + 1]}的距离: {dist:.2f}")
```

### 5.3 数据统计
```python
# 使用列表进行数据统计
scores = [85, 92, 78, 96, 88, 76, 94, 89, 91, 87]

# 计算统计信息
total = sum(scores)
average = total / len(scores)
maximum = max(scores)
minimum = min(scores)

print(f"总分: {total}")
print(f"平均分: {average:.2f}")
print(f"最高分: {maximum}")
print(f"最低分: {minimum}")

# 找出高于平均分的学生
above_average = [score for score in scores if score > average]
print(f"高于平均分的人数: {len(above_average)}")
```

## 6. 常见错误与注意事项

### 6.1 列表的浅拷贝问题
```python
# ❌ 错误：多个变量指向同一个列表
list1 = [1, 2, 3]
list2 = list1
list2.append(4)
print(list1)  # [1, 2, 3, 4] - list1也被修改了！

# ✅ 正确：创建列表的副本
list1 = [1, 2, 3]
list2 = list1.copy()  # 或者 list2 = list1[:]
list2.append(4)
print(list1)  # [1, 2, 3] - list1没有被修改
print(list2)  # [1, 2, 3, 4]
```

### 6.2 元组的单元素问题
```python
# ❌ 错误：这不是元组
single = (42)
print(type(single))  # <class 'int'>

# ✅ 正确：单元素元组需要逗号
single = (42,)
print(type(single))  # <class 'tuple'>
```

### 6.3 索引越界
```python
fruits = ["苹果", "香蕉", "橙子"]

# ❌ 错误：索引越界
# print(fruits[5])  # IndexError

# ✅ 正确：检查索引范围
if len(fruits) > 5:
    print(fruits[5])
else:
    print("索引超出范围")
```

## 重要提示

1. **列表是可变的**：可以修改、添加、删除元素
2. **元组是不可变的**：创建后不能修改，但可以重新赋值
3. **索引从0开始**：第一个元素的索引是0
4. **负数索引**：-1表示最后一个元素
5. **切片操作**：`[start:end:step]`，不包含end位置
6. **内存效率**：元组比列表更节省内存
7. **性能考虑**：元组访问速度比列表快

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
