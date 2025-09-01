## 什么是缩进（Indentation）

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
# 如果你看到这里还不是很懂，没关系
- 现在这个阶段（在接触到if、for等以前 ）
- 只要代码前面空的位置一样多就OK了。