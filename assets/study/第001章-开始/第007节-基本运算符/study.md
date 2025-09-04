# Python 基本运算符

## 一、算术运算符

Python 支持基本的数学运算：

```python
a = 10
b = 3

print(a + b)   # 加法：13
print(a - b)   # 减法：7
print(a * b)   # 乘法：30
print(a / b)   # 除法：3.333...
print(a // b)  # 整除：3
print(a % b)   # 取余：1
print(a ** b)  # 幂运算：1000
```

## 二、比较运算符

用于比较两个值的大小或相等性：

```python
x = 5
y = 3

print(x > y)   # 大于：True
print(x < y)   # 小于：False
print(x >= y)  # 大于等于：True
print(x <= y)  # 小于等于：False
print(x == y)  # 等于：False
print(x != y)  # 不等于：True
```

## 三、逻辑运算符

用于组合多个条件：

```python
a = True
b = False

print(a and b)  # 与运算：False
print(a or b)   # 或运算：True
print(not a)    # 非运算：False
```

## 四、字符串运算符

字符串支持特殊的运算：

```python
s1 = "Hello"
s2 = "World"

print(s1 + s2)  # 字符串拼接：HelloWorld
print(s1 * 3)   # 字符串重复：HelloHelloHello
```

## 五、运算符优先级

运算符有执行顺序，括号可以改变优先级：

```python
result = 2 + 3 * 4    # 先乘后加：14
result = (2 + 3) * 4  # 先加后乘：20
```

## 六、实际应用示例

```python
# 计算圆的面积
radius = 5
pi = 3.14159
area = pi * radius ** 2
print(area)

# 判断数字是否在范围内
num = 15
is_valid = 10 <= num <= 20
print(is_valid)  # True
```

## 注意事项

- 除法 `/` 总是返回浮点数
- 整除 `//` 返回整数（向下取整）
- 字符串只能与字符串拼接
- 使用括号可以明确运算顺序
