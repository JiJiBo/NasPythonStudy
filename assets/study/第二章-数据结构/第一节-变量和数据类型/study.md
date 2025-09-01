# Python 数据类型与变量（Python 3）

## 一、整数（int）

Python 3 可以处理任意大小的整数，包括负数。例如：

```python
a = 1
b = 100
c = -8080
d = 0
```

整数也可以用 **十六进制** 表示，用 `0x` 前缀，例如：

```python
hex_num = 0xff00
print(hex_num)  # 输出 65280
```

---

## 二、浮点数（float）

浮点数就是小数，可以用数学写法或者科学计数法表示：

```python
x = 3.14
y = -9.01
z = 1.23e9     # 相当于 1.23 * 10**9
w = 1.2e-5     # 相当于 0.000012
```

⚠️ 注意：

* **整数运算**是精确的（除法得到浮点数，但整数除法可用 `//`）。
* **浮点数运算**可能有四舍五入误差。

```python
print(0.1 + 0.2)  # 可能输出 0.30000000000000004
```

---

## 三、字符串（str）

字符串用单引号或双引号表示：

```python
s1 = 'abc'
s2 = "xyz"
```

* 引号本身不是字符串的一部分。
* Python 3 的字符串默认是 **Unicode** 编码。

---

## 四、布尔值（bool）

布尔值只有 `True` 和 `False` 两个值：

```python
a = True
b = False
```

布尔运算：

```python
# 与运算
print(True and False)  # False

# 或运算
print(True or False)   # True

# 非运算
print(not True)        # False
```

---

## 五、空值（None）

Python 的空值用 `None` 表示，不等于数字 0：

```python
x = None
print(x)  # 输出 None
```

---

## 六、变量（Variable）

变量是内存中指向数据的名字：

```python
a = 123        # 整数
print(a)       # 123

a = 'Python'   # 字符串
print(a)       # Python
```

⚠️ 注意：

* **Python 是动态类型语言**，同一个变量可以存放不同类型的值。
* **赋值语句的 =** 不是数学等式，而是把右边的值赋给左边变量。

```python
x = 10
x = x + 2  # 先计算 x + 2 = 12，再赋值给 x
print(x)   # 12
```

---

## 七、Raw 字符串与多行字符串

1. **Raw 字符串**（避免转义）：

```python
raw_str = r'\(~_~)/ \(~_~)/'
print(raw_str)
```

2. **多行字符串**（支持换行）：

```python
multi_line = '''Line 1
Line 2
Line 3'''
print(multi_line)
```

3. **Raw 多行字符串**：

```python
raw_multi = r'''Python is created by "Guido".
It is free and easy to learn.
Let's start learn Python!'''
print(raw_multi)
```

---

## 八、补充：变量在内存中的表示

当你写：

```python
a = 'ABC'
```

Python 做了两件事：

1. 在内存中创建 `'ABC'` 字符串。
2. 创建变量 `a`，并指向 `'ABC'`。
 
