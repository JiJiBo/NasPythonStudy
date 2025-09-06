# 📝 Python 类详解

## 1. 什么是类

**类（Class）** 是面向对象编程的核心概念，它是一种**创建对象的蓝图或模板**。类定义了对象的属性和方法，通过类可以创建具有相同结构和行为的多个实例。

## 2. 定义类并创建实例

### 2.1 基本语法
```python
class 类名(object):
    pass
```

### 2.2 简单示例
```python
class Person(object):
    pass
```

按照 Python 的编程习惯，类名以大写字母开头，紧接着是 `(object)`，表示该类是从哪个类继承下来的。类的继承将在后面的章节讲解，现在我们只需要简单地从 object 类继承。

### 2.3 创建实例
有了 Person 类的定义，就可以创建出具体的实例。创建实例使用 `类名+()`，类似函数调用的形式创建：

```python
Bob = Person()
Jeff = Person()

print(Bob)  # <__main__.Person object at 0x...>
print(Jeff)  # <__main__.Person object at 0x...>
print(Bob == Jeff)  # False，不同的实例
```

## 3. 实例属性

### 3.1 动态添加属性
由于 Python 是动态语言，对每一个实例，都可以直接给他们的属性赋值：

```python
Bob.sex = 'male'
Jeff.sex = 'female'

print(Bob.sex)  # male
print(Jeff.sex)  # female
```

### 3.2 实例属性的特点
- 每个实例的属性是独立的
- 修改一个实例的属性不会影响其他实例
- 可以随时添加新属性

```python
Bob.age = 25
Jeff.age = 30

print(Bob.age)  # 25
print(Jeff.age)  # 30
```

## 4. 初始化实例属性

### 4.1 __init__ 方法
在定义 Person 类时，可以为 Person 类添加一个特殊的 `__init__()` 方法，当创建实例时，`__init__()` 方法被自动调用，我们就能在此为每个实例都统一加上以下属性：

```python
class Person(object):
    def __init__(self, name, gender, birth):
        self.name = name
        self.gender = gender
        self.birth = birth
```

### 4.2 参数说明
- `__init__()` 方法的第一个参数必须是 `self`（也可以用别的名字，但建议使用习惯用法）
- 后续参数则可以自由指定，和定义函数没有任何区别
- `self` 指向创建的实例本身

### 4.3 创建实例
相应地，创建实例时，就必须要提供除 self 以外的参数：

```python
xiaoming = Person('Xiao Ming', 'Male', '1991-1-1')
xiaohong = Person('Xiao Hong', 'Female', '1992-2-2')

print(xiaoming.name)    # Xiao Ming
print(xiaoming.gender)  # Male
print(xiaoming.birth)   # 1991-1-1

print(xiaohong.name)    # Xiao Hong
print(xiaohong.gender)  # Female
print(xiaohong.birth)   # 1992-2-2
```

### 4.4 私有属性
注意，实例属性若以双下划线 `__` 开头，则被视为私有属性，不允许外部访问：

```python
class Person(object):
    def __init__(self, name, gender, birth):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.__id = 12345  # 私有属性

xiaoming = Person('Xiao Ming', 'Male', '1991-1-1')
print(xiaoming.name)  # Xiao Ming
# print(xiaoming.__id)  # AttributeError: 'Person' object has no attribute '__id'
```

## 5. 类属性

### 5.1 定义类属性
绑定在一个实例上的属性不会影响其他实例，但是，类本身也是一个对象，如果在类上绑定一个属性，则所有实例都可以访问类的属性，并且，所有实例访问的类属性都是同一个！

定义类属性可以直接在 class 中定义：

```python
class Person(object):
    address = 'Earth'  # 类属性
    
    def __init__(self, name):
        self.name = name  # 实例属性

# 创建实例
p1 = Person('Bob')
p2 = Person('Alice')

print(p1.address)  # Earth
print(p2.address)  # Earth
print(Person.address)  # Earth

# 修改类属性
Person.address = 'Mars'
print(p1.address)  # Mars
print(p2.address)  # Mars
```

### 5.2 实例属性 vs 类属性
当实例属性和类属性重名时，实例属性优先级高，它将屏蔽掉对类属性的访问：

```python
class Person(object):
    name = 'Person'  # 类属性
    
    def __init__(self, name):
        self.name = name  # 实例属性

p1 = Person('Bob')
print(p1.name)      # Bob（实例属性）
print(Person.name)  # Person（类属性）
```

## 6. 实例方法

### 6.1 定义实例方法
一个实例的私有属性就是以 `__` 开头的属性，无法被外部访问，那这些属性定义有什么用？

虽然私有属性无法从外部访问，但是，从类的内部是可以访问的。除了可以定义实例的属性外，还可以定义实例的方法。

实例的方法就是在类中定义的函数，它的第一个参数永远是 `self`，指向调用该方法的实例本身，其他参数和一个普通函数是完全一样的：

```python
class Person(object):
    def __init__(self, name):
        self.__name = name  # 私有属性

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    def introduce(self):
        return f"我的名字是 {self.__name}"
```

### 6.2 调用实例方法
`get_name(self)` 就是一个实例方法，它的第一个参数是 self。`__init__(self, name)` 其实也可看做是一个特殊的实例方法。

调用实例方法必须在实例上调用：

```python
p1 = Person('Bob')
print(p1.get_name())  # Bob（self不需要显式传入）
print(p1.introduce())  # 我的名字是 Bob

p1.set_name('Alice')
print(p1.get_name())  # Alice
```

### 6.3 数据封装
在实例方法内部，可以访问所有实例属性，这样，如果外部需要访问私有属性，可以通过方法调用获得，这种数据封装的形式除了能保护内部数据一致性外，还可以简化外部调用的难度：

```python
class BankAccount(object):
    def __init__(self, initial_balance):
        self.__balance = initial_balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.__balance

# 使用
account = BankAccount(1000)
print(account.get_balance())  # 1000

account.deposit(500)
print(account.get_balance())  # 1500

account.withdraw(200)
print(account.get_balance())  # 1300
```

## 7. 类方法

### 7.1 定义类方法
在 class 中定义的全部是实例方法，实例方法第一个参数 self 是实例本身。

要在 class 中定义类方法，需要这么写：

```python
class Person(object):
    count = 0  # 类属性
    
    @classmethod
    def how_many(cls):
        return cls.count
    
    def __init__(self, name):
        self.name = name
        Person.count = Person.count + 1

print(Person.how_many())  # 0
p1 = Person('Bob')
print(Person.how_many())  # 1
p2 = Person('Alice')
print(Person.how_many())  # 2
```

### 7.2 类方法的特点
通过标记一个 `@classmethod`，该方法将绑定到 Person 类上，而非类的实例。类方法的第一个参数将传入类本身，通常将参数名命名为 `cls`，上面的 `cls.count` 实际上相当于 `Person.count`。

因为是在类上调用，而非实例上调用，因此类方法无法获得任何实例变量，只能获得类的引用：

```python
class Person(object):
    count = 0
    
    @classmethod
    def get_count(cls):
        return cls.count
    
    @classmethod
    def reset_count(cls):
        cls.count = 0
    
    def __init__(self, name):
        self.name = name
        Person.count += 1

# 类方法调用
print(Person.get_count())  # 0

p1 = Person('Bob')
p2 = Person('Alice')
print(Person.get_count())  # 2

Person.reset_count()
print(Person.get_count())  # 0
```

## 8. 静态方法

### 8.1 定义静态方法
静态方法不需要访问类或实例的任何属性，使用 `@staticmethod` 装饰器：

```python
class MathUtils(object):
    @staticmethod
    def add(x, y):
        return x + y
    
    @staticmethod
    def multiply(x, y):
        return x * y

# 调用静态方法
result1 = MathUtils.add(3, 5)  # 8
result2 = MathUtils.multiply(4, 6)  # 24

# 也可以通过实例调用
math = MathUtils()
result3 = math.add(2, 3)  # 5
```

## 9. 实际应用示例

### 9.1 学生管理系统
```python
class Student(object):
    school = "Python大学"  # 类属性
    
    def __init__(self, name, student_id, grade):
        self.name = name
        self.student_id = student_id
        self.grade = grade
        self.__courses = []  # 私有属性
    
    def add_course(self, course):
        self.__courses.append(course)
    
    def get_courses(self):
        return self.__courses.copy()
    
    def get_info(self):
        return f"姓名: {self.name}, 学号: {self.student_id}, 年级: {self.grade}"
    
    @classmethod
    def get_school(cls):
        return cls.school

# 使用
student1 = Student("张三", "2023001", "大一")
student2 = Student("李四", "2023002", "大一")

student1.add_course("Python编程")
student1.add_course("数据结构")

print(student1.get_info())
print(student1.get_courses())
print(Student.get_school())
```

### 9.2 银行账户系统
```python
class BankAccount(object):
    interest_rate = 0.02  # 年利率
    
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.__balance = initial_balance
        self.__transactions = []
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.__transactions.append(f"存款: +{amount}")
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transactions.append(f"取款: -{amount}")
            return True
        return False
    
    def get_balance(self):
        return self.__balance
    
    def get_transactions(self):
        return self.__transactions.copy()
    
    @classmethod
    def set_interest_rate(cls, rate):
        cls.interest_rate = rate
    
    def calculate_interest(self):
        return self.__balance * BankAccount.interest_rate

# 使用
account = BankAccount("123456789", 1000)
account.deposit(500)
account.withdraw(200)
print(f"余额: {account.get_balance()}")
print(f"交易记录: {account.get_transactions()}")
```

## 10. 常见错误与注意事项

### 10.1 忘记 self 参数
```python
# ❌ 错误
class Person(object):
    def get_name():  # 缺少 self 参数
        return self.name

# ✅ 正确
class Person(object):
    def get_name(self):
        return self.name
```

### 10.2 混淆类属性和实例属性
```python
class Person(object):
    name = "Person"  # 类属性
    
    def __init__(self, name):
        self.name = name  # 实例属性

p1 = Person("Bob")
print(p1.name)      # Bob（实例属性）
print(Person.name)  # Person（类属性）
```

### 10.3 私有属性访问
```python
class Person(object):
    def __init__(self, name):
        self.__name = name  # 私有属性

p1 = Person("Bob")
# print(p1.__name)  # AttributeError
print(p1._Person__name)  # Bob（不推荐，但可以访问）
```

## 重要提示

1. **类名**：使用大写字母开头的驼峰命名法
2. **实例属性**：每个实例独立拥有
3. **类属性**：所有实例共享
4. **私有属性**：以双下划线开头，外部无法直接访问
5. **实例方法**：第一个参数必须是 self
6. **类方法**：使用 @classmethod 装饰器，第一个参数是 cls
7. **静态方法**：使用 @staticmethod 装饰器，不需要 self 或 cls
8. **数据封装**：通过方法控制对私有属性的访问

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
