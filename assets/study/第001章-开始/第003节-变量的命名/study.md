## Python 变量命名规则

1. **首字符限制**
    - 必须以字母（a-z, A-Z）或下划线 `_` 开头。
    - ✅ 示例：`name`, `_temp`, `User1`
    - ❌ 错误：`1stValue`, `@abc`

2. **组成部分**
    - 之后的字符可以是 **字母、数字、下划线**。
    - ✅ 示例：`score_1`, `student_name`, `age20`

3. **大小写敏感**
    - `count` 和 `Count` 是不同的变量。
    - ✅ 可以共存：

   ```python
   count = 10
   Count = 20
   ```

4. **长度建议**
    - 没有硬性限制，但推荐 ≤ 20 个字符，保持可读性。
    - ✅ 好：`max_score`
    - ❌ 不好：`the_maximum_score_of_all_students_in_the_exam`

5. **禁止使用关键字**
    - 例如：`if`, `for`, `class`, `def`, `import` 等不能作为变量名。
    - 可以通过 `keyword` 模块查看所有关键字：

   ```python
   import keyword
   print(keyword.kwlist)
   ```

---

## 变量命名风格（Python 社区约定）

1. **小写字母 + 下划线**（snake\_case）
    - 推荐：`student_name`, `max_value`

2. **常量用全大写**
    - `PI = 3.14159`, `MAX_SPEED = 120`

3. **类名用大驼峰**（PascalCase）
    - `class StudentInfo:`

4. **私有变量用下划线开头**
    - `_hidden_value = 42`

---

## 常见命名错误

```python
# ❌ 以数字开头
2value = 10

# ❌ 使用特殊字符
user - name = "Tom"


# ❌ 使用关键字
class = "Math"  
```

# 你可以在底下的代码编辑器中，输入你的代码。
![img.png](./assets/01-03/img.png)- 

# 然后，点击按钮，交由AI评论