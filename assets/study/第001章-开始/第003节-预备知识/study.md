---

## 1. 什么是赋值（Assignment）

在 Python 中，**赋值**就是把一个数据保存到变量里。
语法是：

```python
变量名 = 值
```

示例：

```python
x = 10       # 把数字10赋值给变量x
name = "Neo" # 把字符串"Neo"赋值给变量name
y = x + 5    # 先计算x+5，再赋值给变量y
```

特点：

* `=` 在 Python 里不是数学的“等于”，而是 **赋值符号**。
* 变量本身只是一个 **名字**，它指向内存中的某个值。

---

## 2. 什么是缩进（Indentation）

在 Python 中，**缩进**是语法的一部分。
其他语言可能用大括号 `{}` 来表示代码块，而 Python **强制用缩进**。

规则：

* 一般使用 **4个空格** 作为缩进（不要混用 Tab 和空格）。
* 相同层级的代码，必须缩进一致。

示例：

```python
score = 75

if score >= 60:
    print("及格")  # 这里缩进4个空格
    print("继续加油")  # 和上面保持同级缩进
else:
    print("不及格")
```

如果缩进不一致，会报错：

```python
IndentationError: unexpected
indent
```

---

## 3. 什么是 `pass`

`pass` 是 Python 的 **占位语句**，表示“这里暂时什么都不做”。
它通常用于：

* 占位，保持语法结构完整。
* 提前写好框架，功能以后再补。

示例：

```python
def todo_function():
    pass  # 暂时不写内容，避免报错
```

如果不写 `pass`，Python 会报错：

```python
def todo_function():
# 空函数会报错
```

报错内容：

```
IndentationError: expected an indented block
```

---

✅ 总结：

* **赋值**：`=` 把值存到变量。
* **缩进**：用空格控制代码块结构，Python语法强制要求。
* **pass**：占位语句，表示“啥也不干，但语法完整”。

---
 