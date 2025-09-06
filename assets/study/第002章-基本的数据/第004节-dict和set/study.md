# 🗂️ Python Dict 和 Set 详解

## 1. 字典 (Dictionary) - 键值对映射

### 1.1 什么是字典
字典是 Python 中最重要的数据类型之一，它是一个**无序的、可变的**键值对集合。字典通过键来快速查找值。

### 1.2 创建字典
```python
# 空字典
empty_dict = {}
empty_dict2 = dict()

# 包含键值对的字典
student = {
    "name": "张三",
    "age": 20,
    "grade": "A"
}

# 使用 dict() 函数
student2 = dict(name="李四", age=19, grade="B")

# 从列表创建字典
keys = ["name", "age", "grade"]
values = ["王五", 21, "A"]
student3 = dict(zip(keys, values))
```

### 1.3 访问字典元素
```python
student = {
    "name": "张三",
    "age": 20,
    "grade": "A",
    "subjects": ["数学", "英语", "物理"]
}

# 通过键访问值
print(student["name"])        # 张三
print(student["age"])         # 20

# 使用 get() 方法（推荐）
print(student.get("name"))    # 张三
print(student.get("phone"))   # None（键不存在时返回None）
print(student.get("phone", "未知"))  # 未知（提供默认值）

# 访问嵌套值
print(student["subjects"][0])  # 数学
```

### 1.4 修改字典元素
```python
student = {"name": "张三", "age": 20}

# 修改现有键的值
student["age"] = 21

# 添加新的键值对
student["grade"] = "A"
student["phone"] = "13800138000"

print(student)  # {'name': '张三', 'age': 21, 'grade': 'A', 'phone': '13800138000'}
```

### 1.5 字典常用方法

#### 获取键、值、键值对
```python
student = {"name": "张三", "age": 20, "grade": "A"}

# 获取所有键
keys = student.keys()
print(list(keys))  # ['name', 'age', 'grade']

# 获取所有值
values = student.values()
print(list(values))  # ['张三', 20, 'A']

# 获取所有键值对
items = student.items()
print(list(items))  # [('name', '张三'), ('age', 20), ('grade', 'A')]
```

#### 删除元素
```python
student = {"name": "张三", "age": 20, "grade": "A"}

# pop() - 删除并返回指定键的值
age = student.pop("age")
print(age)      # 20
print(student)  # {'name': '张三', 'grade': 'A'}

# popitem() - 删除并返回最后一个键值对
last_item = student.popitem()
print(last_item)  # ('grade', 'A')
print(student)    # {'name': '张三'}

# del 语句
del student["name"]
print(student)  # {}

# clear() - 清空字典
student = {"name": "张三", "age": 20}
student.clear()
print(student)  # {}
```

#### 更新字典
```python
student1 = {"name": "张三", "age": 20}
student2 = {"age": 21, "grade": "A"}

# update() - 更新字典
student1.update(student2)
print(student1)  # {'name': '张三', 'age': 21, 'grade': 'A'}

# 直接赋值更新
student1.update({"phone": "13800138000"})
print(student1)  # {'name': '张三', 'age': 21, 'grade': 'A', 'phone': '13800138000'}
```

### 1.6 字典推导式
```python
# 基本语法：{键表达式: 值表达式 for 变量 in 序列}
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 带条件的字典推导式
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squares)  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}

# 从列表创建字典
fruits = ["苹果", "香蕉", "橙子"]
fruit_prices = {fruit: len(fruit) * 2 for fruit in fruits}
print(fruit_prices)  # {'苹果': 4, '香蕉': 4, '橙子': 4}
```

## 2. 集合 (Set) - 无序唯一元素

### 2.1 什么是集合
集合是一个**无序的、不重复的**元素集合。集合主要用于去重和集合运算。

### 2.2 创建集合
```python
# 空集合
empty_set = set()  # 注意：不能用 {} 创建空集合，那会创建空字典

# 包含元素的集合
fruits = {"苹果", "香蕉", "橙子"}
numbers = {1, 2, 3, 4, 5}

# 从列表创建集合（自动去重）
numbers_list = [1, 2, 2, 3, 3, 4, 5]
unique_numbers = set(numbers_list)
print(unique_numbers)  # {1, 2, 3, 4, 5}

# 从字符串创建集合
chars = set("hello")
print(chars)  # {'h', 'e', 'l', 'o'}  # 注意：'l' 只出现一次
```

### 2.3 访问集合元素
```python
fruits = {"苹果", "香蕉", "橙子"}

# 集合不支持索引访问
# print(fruits[0])  # 错误！

# 遍历集合
for fruit in fruits:
    print(fruit)

# 检查元素是否存在
print("苹果" in fruits)  # True
print("葡萄" in fruits)  # False
```

### 2.4 修改集合元素
```python
fruits = {"苹果", "香蕉"}

# add() - 添加单个元素
fruits.add("橙子")
print(fruits)  # {'苹果', '香蕉', '橙子'}

# update() - 添加多个元素
fruits.update(["葡萄", "草莓"])
print(fruits)  # {'苹果', '香蕉', '橙子', '葡萄', '草莓'}

# remove() - 删除指定元素（元素不存在会报错）
fruits.remove("香蕉")
print(fruits)  # {'苹果', '橙子', '葡萄', '草莓'}

# discard() - 删除指定元素（元素不存在不会报错）
fruits.discard("西瓜")  # 不会报错
fruits.discard("苹果")
print(fruits)  # {'橙子', '葡萄', '草莓'}

# pop() - 删除并返回任意一个元素
removed = fruits.pop()
print(f"删除了: {removed}")
print(fruits)

# clear() - 清空集合
fruits.clear()
print(fruits)  # set()
```

### 2.5 集合运算
```python
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

# 并集 (union)
union = set1 | set2
print(union)  # {1, 2, 3, 4, 5, 6, 7, 8}

# 交集 (intersection)
intersection = set1 & set2
print(intersection)  # {4, 5}

# 差集 (difference)
difference = set1 - set2
print(difference)  # {1, 2, 3}

# 对称差集 (symmetric difference)
symmetric_diff = set1 ^ set2
print(symmetric_diff)  # {1, 2, 3, 6, 7, 8}

# 子集和超集
set3 = {1, 2, 3}
print(set3.issubset(set1))    # True
print(set1.issuperset(set3))  # True
```

### 2.6 集合推导式
```python
# 基本语法：{表达式 for 变量 in 序列}
squares = {x**2 for x in range(1, 6)}
print(squares)  # {1, 4, 9, 16, 25}

# 带条件的集合推导式
even_squares = {x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squares)  # {64, 4, 36, 100, 16}
```

## 3. 字典 vs 集合

### 3.1 主要区别
| 特性 | 字典 (Dict) | 集合 (Set) |
|------|-------------|------------|
| 元素类型 | 键值对 | 单个元素 |
| 访问方式 | 通过键 | 遍历或成员检查 |
| 重复元素 | 键唯一，值可重复 | 元素唯一 |
| 语法 | `{key: value}` | `{element}` |
| 空对象 | `{}` | `set()` |

### 3.2 使用场景
```python
# 字典适用于需要键值映射的场景
student_grades = {
    "张三": 85,
    "李四": 92,
    "王五": 78
}

# 集合适用于去重和集合运算的场景
unique_names = {"张三", "李四", "王五", "张三"}  # 自动去重
print(unique_names)  # {'张三', '李四', '王五'}
```

## 4. 嵌套结构

### 4.1 嵌套字典
```python
# 学生信息管理系统
students = {
    "001": {
        "name": "张三",
        "age": 20,
        "grades": {
            "数学": 85,
            "英语": 92,
            "物理": 78
        }
    },
    "002": {
        "name": "李四",
        "age": 19,
        "grades": {
            "数学": 90,
            "英语": 88,
            "物理": 95
        }
    }
}

# 访问嵌套数据
print(students["001"]["name"])           # 张三
print(students["001"]["grades"]["数学"])  # 85
```

### 4.2 字典和集合混合
```python
# 课程管理系统
courses = {
    "数学": {"students": {"张三", "李四", "王五"}, "teacher": "刘老师"},
    "英语": {"students": {"张三", "赵六"}, "teacher": "陈老师"},
    "物理": {"students": {"李四", "王五", "赵六"}, "teacher": "王老师"}
}

# 查找同时选修数学和英语的学生
math_students = courses["数学"]["students"]
english_students = courses["英语"]["students"]
both_subjects = math_students & english_students
print(f"同时选修数学和英语的学生: {both_subjects}")
```

## 5. 实际应用示例

### 5.1 词频统计
```python
# 统计文本中每个单词的出现次数
text = "python is great python is powerful python is easy"
words = text.split()

word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

print("词频统计:")
for word, count in word_count.items():
    print(f"{word}: {count}")

# 使用 collections.Counter 更简洁
from collections import Counter
word_count2 = Counter(words)
print("使用Counter:", dict(word_count2))
```

### 5.2 数据去重
```python
# 从列表中去除重复元素
numbers = [1, 2, 2, 3, 3, 4, 5, 5, 6]
unique_numbers = list(set(numbers))
print(f"原列表: {numbers}")
print(f"去重后: {unique_numbers}")

# 保持原有顺序的去重
seen = set()
unique_ordered = []
for num in numbers:
    if num not in seen:
        seen.add(num)
        unique_ordered.append(num)
print(f"保持顺序去重: {unique_ordered}")
```

### 5.3 用户权限管理
```python
# 用户权限系统
users = {
    "admin": {"permissions": {"read", "write", "delete", "admin"}, "role": "管理员"},
    "editor": {"permissions": {"read", "write"}, "role": "编辑"},
    "viewer": {"permissions": {"read"}, "role": "查看者"}
}

def check_permission(username, permission):
    if username in users:
        return permission in users[username]["permissions"]
    return False

# 测试权限
print(check_permission("admin", "delete"))  # True
print(check_permission("editor", "delete"))  # False
print(check_permission("viewer", "read"))    # True
```

### 5.4 数据分析
```python
# 学生成绩分析
student_scores = {
    "张三": [85, 92, 78, 96],
    "李四": [90, 88, 95, 87],
    "王五": [76, 84, 89, 82],
    "赵六": [94, 91, 88, 93]
}

# 计算每个学生的平均分
averages = {}
for student, scores in student_scores.items():
    averages[student] = sum(scores) / len(scores)

print("学生平均分:")
for student, avg in averages.items():
    print(f"{student}: {avg:.2f}")

# 找出平均分最高的学生
best_student = max(averages, key=averages.get)
print(f"平均分最高的学生: {best_student} ({averages[best_student]:.2f})")
```

## 6. 常见错误与注意事项

### 6.1 字典键的类型限制
```python
# ✅ 正确：字符串、数字、元组可以作为键
valid_dict = {
    "name": "张三",
    123: "数字键",
    (1, 2): "元组键"
}

# ❌ 错误：列表不能作为键
# invalid_dict = {[1, 2]: "列表键"}  # TypeError

# ✅ 正确：任何类型都可以作为值
mixed_values = {
    "string": "字符串值",
    "number": 123,
    "list": [1, 2, 3],
    "dict": {"nested": "value"}
}
```

### 6.2 集合元素类型限制
```python
# ✅ 正确：不可变类型可以作为集合元素
valid_set = {1, 2, 3, "hello", (1, 2)}

# ❌ 错误：可变类型不能作为集合元素
# invalid_set = {[1, 2], {1: 2}}  # TypeError
```

### 6.3 空集合创建
```python
# ❌ 错误：{} 创建的是空字典，不是空集合
empty_dict = {}
print(type(empty_dict))  # <class 'dict'>

# ✅ 正确：使用 set() 创建空集合
empty_set = set()
print(type(empty_set))   # <class 'set'>
```

### 6.4 字典访问不存在的键
```python
student = {"name": "张三", "age": 20}

# ❌ 错误：访问不存在的键会报错
# print(student["grade"])  # KeyError

# ✅ 正确：使用 get() 方法
print(student.get("grade"))        # None
print(student.get("grade", "未知"))  # 未知
```

## 重要提示

1. **字典的键必须唯一且不可变**：字符串、数字、元组可以作为键
2. **集合的元素必须唯一且不可变**：不能包含列表、字典等可变类型
3. **字典和集合都是无序的**：Python 3.7+ 字典保持插入顺序
4. **性能优势**：字典和集合的查找、插入、删除操作都是 O(1) 平均时间复杂度
5. **内存效率**：集合比列表更节省内存，特别是对于大量唯一元素
6. **去重功能**：集合天然具有去重功能
7. **集合运算**：集合支持丰富的数学集合运算

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
