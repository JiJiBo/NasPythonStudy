## 什么是 `pass`

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
 