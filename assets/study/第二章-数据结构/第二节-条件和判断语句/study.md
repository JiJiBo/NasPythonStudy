### 1、`if`、`elif`、`else` 语句（Python 3）

```python
# if语句
score = 75
if score >= 60:
    print('passed')

# else-if语句（Python中是if-else）
score = 55
if score >= 60:
    print('passed')
else:
    print('failed')

# if-elif-else语句
score = 85
if score >= 90:
    print('excellent')
elif score >= 80:
    print('good')
elif score >= 60:
    print('passed')
else:
    print('failed')
```

---

### 2、`for` 循环（Python 3）

```python
scores = [75, 92, 59, 68]
total = 0.0
for score in scores:
    total += score

average = total / len(scores)
print("Average score:", average)
```
 