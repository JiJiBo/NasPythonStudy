# 字符串操作

## 一、字符串长度

使用 `len()` 函数获取字符串的长度：

```python
text = "Hello World"
length = len(text)
print(length)  # 输出：11
```

## 二、字符串索引

字符串中的每个字符都有位置编号，从0开始：

```python
text = "Python"
print(text[0])   # 输出：P
print(text[1])   # 输出：y
print(text[-1])  # 输出：n（倒数第一个）
print(text[-2])  # 输出：o（倒数第二个）
```

## 三、字符串切片

使用 `[开始:结束:步长]` 来获取字符串的一部分：

```python
text = "Hello World"

# 基本切片
print(text[0:5])    # 输出：Hello
print(text[:5])     # 输出：Hello（从开头到第5个）
print(text[6:])     # 输出：World（从第6个到结尾）
print(text[-5:])    # 输出：World（最后5个字符）

# 步长切片
print(text[::2])    # 输出：HloWrd（每隔一个字符）
print(text[::-1])   # 输出：dlroW olleH（反转字符串）
```

## 四、字符串常用方法

### 1. 大小写转换

```python
text = "Hello World"
print(text.upper())    # 输出：HELLO WORLD
print(text.lower())    # 输出：hello world
print(text.title())    # 输出：Hello World
```

### 2. 去除空白字符

```python
text = "  Hello World  "
print(text.strip())    # 输出：Hello World（去除两边空格）
print(text.lstrip())   # 输出：Hello World （去除左边空格）
print(text.rstrip())   # 输出： Hello World（去除右边空格）
```

### 3. 字符串分割

```python
text = "apple,banana,orange"
fruits = text.split(",")
print(fruits)  # 输出：['apple', 'banana', 'orange']

# 分割成列表后可以访问元素
print(fruits[0])  # 输出：apple
```

### 4. 字符串替换

```python
text = "Hello World"
new_text = text.replace("World", "Python")
print(new_text)  # 输出：Hello Python
```

### 5. 字符串查找

```python
text = "Hello World"
print(text.find("World"))    # 输出：6（找到的位置）
print(text.find("Python"))   # 输出：-1（没找到）
print("World" in text)       # 输出：True（是否包含）
```

## 五、字符串拼接

```python
# 使用 + 拼接
first = "Hello"
second = "World"
result = first + " " + second
print(result)  # 输出：Hello World

# 使用 join 方法
words = ["Hello", "World", "Python"]
result = " ".join(words)
print(result)  # 输出：Hello World Python
```

## 六、实际应用示例

```python
# 处理用户输入
user_input = "  hello world  "
cleaned_input = user_input.strip().title()
print(cleaned_input)  # 输出：Hello World

# 检查文件扩展名
filename = "document.txt"
if filename.endswith(".txt"):
    print("这是一个文本文件")

# 分割CSV数据
csv_line = "张三,25,北京"
name, age, city = csv_line.split(",")
print(f"姓名：{name}，年龄：{age}，城市：{city}")
```

## 注意事项

- 字符串是不可变的，所有方法都返回新的字符串
- 索引从0开始，负数索引从-1开始
- 切片 `[开始:结束]` 包含开始位置，不包含结束位置
- 字符串方法不会修改原字符串，需要重新赋值
