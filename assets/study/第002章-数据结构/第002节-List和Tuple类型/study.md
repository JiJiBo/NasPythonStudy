# Python 中的 List 和 Tuple

## 1、List（列表）

* 等价于 JavaScript 的数组，用 **中括号 `[]`** 包裹，元素用 **逗号 `,`** 分隔。
  例如：

  ```python
  ['Adam', 95.5, 'Lisa', 85, 'Bart', 59]
  ```

* **访问元素**
  使用索引访问：

  ```python
  L = [95.5, 85, 62, 59]
  print(L[0])  # 正序索引，下标从 0 开始
  print(L[-1]) # 倒序索引，下标从 -1 开始
  ```

* **常用方法**：

    * `.append(item)`
      往列表末尾添加元素（等价于 JS 的 `push()`）

      ```python
      L.append(100)
      ```

    * `.insert(index, item)`
      在指定索引位置插入元素

      ```python
      L.insert(1, 90)  # 在索引1位置插入90
      ```

    * `.pop(index=-1)`
      删除并返回指定位置的元素，不传参数则默认删除末尾元素

      ```python
      L.pop()    # 删除并返回末尾元素
      L.pop(0)   # 删除并返回索引0元素
      ```

---

## 2、Tuple（元组）

* 元组是一种**有序、不可变**的序列，创建后不能修改。

* 使用 **圆括号 `()`** 创建：

  ```python
  t = ('Adam', 'Lisa', 'Bart')
  ```

* **特点**：

    * 元组没有 `.append()`、`.insert()`、`.pop()` 等方法
      → 不能直接添加或删除元素
    * 元组元素访问与列表一样：

      ```python
      print(t[0])  # 'Adam'
      print(t[-1]) # 'Bart'
      ```
    * 不能通过赋值修改元素：

      ```python
      t[0] = 'Jack'  # 会报错
      ```

* **单元素元组**：

    * 必须在元素后加逗号 `,`，否则 Python 会把括号当作普通括号：

      ```python
      single = ('Jrain',)
      ```
 
好的，我来出一道结合 **List** 和 **Tuple** 的练习题，难度适中，并能考察索引和方法使用：

---

明白了，我给你设计一个**函数型题目**，只返回一个结果，不涉及多步输出。

---

### 题目：

已知一个班级学生和成绩：

```python
students = ['Adam', 'Lisa', 'Bart', 'Jrain']
scores = (95, 85, 59, 100)
```

请写一个函数 `top_student(students, scores)`，返回**成绩最高的学生姓名**。

* 输入：两个序列 `students`（列表）和 `scores`（元组）
* 输出：字符串，表示成绩最高的学生姓名

#### 示例：

```python
top_student(['Adam', 'Lisa', 'Bart', 'Jrain'], (95, 85, 59, 100))
# 返回: 'Jrain'
```
 
