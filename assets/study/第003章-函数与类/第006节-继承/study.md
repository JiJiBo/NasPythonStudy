# 📝 Python 继承详解

## 1. 什么是继承

**继承（Inheritance）** 是面向对象编程的重要特性之一，它允许一个类（子类）继承另一个类（父类）的属性和方法。通过继承，子类可以重用父类的代码，同时可以添加或修改自己的功能。

## 2. 单继承

### 2.1 基本语法
```python
class 子类名(父类名):
    pass
```

### 2.2 简单示例
如果已经定义了 Person 类，需要定义新的 Student 和 Teacher 类时，可以直接从 Person 类继承：

```python
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
    
    def introduce(self):
        return f"我是 {self.name}，性别 {self.gender}"

# 定义Student类时，只需要把额外的属性加上，例如score
class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score
    
    def get_grade(self):
        if self.score >= 90:
            return "优秀"
        elif self.score >= 80:
            return "良好"
        elif self.score >= 70:
            return "中等"
        else:
            return "及格"

# 定义Teacher类
class Teacher(Person):
    def __init__(self, name, gender, subject):
        super(Teacher, self).__init__(name, gender)
        self.subject = subject
    
    def teach(self):
        return f"{self.name} 老师正在教授 {self.subject}"
```

### 2.3 使用super()函数
一定要用 `super(Student, self).__init__(name, gender)` 去初始化父类，否则，继承自 Person 的 Student 将没有 name 和 gender。

函数 `super(Student, self)` 将返回当前类继承的父类，即 Person，然后调用 `__init__()` 方法，注意 self 参数已在 super() 中传入，在 `__init__()` 中将隐式传递，不需要写出（也不能写）。

相应地，创建实例时，就必须要提供除 self 以外的参数：

```python
xiaoming = Student('Xiao Ming', 'Male', 95)
xiaohong = Teacher('Xiao Hong', 'Female', 'Math')

print(xiaoming.introduce())  # 我是 Xiao Ming，性别 Male
print(xiaoming.get_grade())  # 优秀

print(xiaohong.introduce())  # 我是 Xiao Hong，性别 Female
print(xiaohong.teach())      # Xiao Hong 老师正在教授 Math
```

## 3. 多重继承

### 3.1 基本语法
除了从一个父类继承外，Python 允许从多个父类继承，称为多重继承：

```python
class 子类名(父类1, 父类2, ...):
    pass
```

### 3.2 多重继承示例
```python
class A(object):
    def __init__(self, a):
        print('init A...')
        self.a = a
    
    def method_a(self):
        return f"A类方法: {self.a}"

class B(A):
    def __init__(self, a):
        super(B, self).__init__(a)
        print('init B...')
    
    def method_b(self):
        return f"B类方法: {self.a}"

class C(A):
    def __init__(self, a):
        super(C, self).__init__(a)
        print('init C...')
    
    def method_c(self):
        return f"C类方法: {self.a}"

class D(B, C):
    def __init__(self, a):
        super(D, self).__init__(a)
        print('init D...')
    
    def method_d(self):
        return f"D类方法: {self.a}"
```

### 3.3 方法解析顺序（MRO）
像这样，D 同时继承自 B 和 C，也就是 D 拥有了 A、B、C 的全部功能。多重继承通过 super() 调用 `__init__()` 方法时，A 虽然被继承了两次，但 `__init__()` 只调用一次：

```python
d = D('d')
# 输出：
# init A...
# init C...
# init B...
# init D...

print(d.method_a())  # A类方法: d
print(d.method_b())  # B类方法: d
print(d.method_c())  # C类方法: d
print(d.method_d())  # D类方法: d
```

### 3.4 查看MRO
可以使用 `__mro__` 属性查看方法解析顺序：

```python
print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

## 4. 方法重写

### 4.1 重写父类方法
子类可以重写父类的方法，提供自己的实现：

```python
class Animal(object):
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return "动物发出声音"
    
    def move(self):
        return f"{self.name} 在移动"

class Dog(Animal):
    def __init__(self, name, breed):
        super(Dog, self).__init__(name)
        self.breed = breed
    
    def make_sound(self):  # 重写父类方法
        return f"{self.name} 汪汪叫"
    
    def fetch(self):
        return f"{self.name} 在捡球"

class Cat(Animal):
    def __init__(self, name, color):
        super(Cat, self).__init__(name)
        self.color = color
    
    def make_sound(self):  # 重写父类方法
        return f"{self.name} 喵喵叫"
    
    def climb(self):
        return f"{self.name} 在爬树"

# 使用
dog = Dog("旺财", "金毛")
cat = Cat("咪咪", "橘色")

print(dog.make_sound())  # 旺财 汪汪叫
print(cat.make_sound())  # 咪咪 喵喵叫
print(dog.move())        # 旺财 在移动（继承自父类）
print(cat.move())        # 咪咪 在移动（继承自父类）
```

### 4.2 调用父类方法
在重写的方法中，可以使用 `super()` 调用父类的方法：

```python
class Vehicle(object):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start(self):
        return f"{self.brand} {self.model} 启动"
    
    def stop(self):
        return f"{self.brand} {self.model} 停止"

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super(Car, self).__init__(brand, model)
        self.doors = doors
    
    def start(self):
        # 调用父类方法并添加额外功能
        parent_result = super(Car, self).start()
        return f"{parent_result}，车门数: {self.doors}"

car = Car("丰田", "凯美瑞", 4)
print(car.start())  # 丰田 凯美瑞 启动，车门数: 4
print(car.stop())   # 丰田 凯美瑞 停止
```

## 5. 属性继承

### 5.1 实例属性继承
```python
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__private_attr = "私有属性"  # 私有属性
    
    def get_private_attr(self):
        return self.__private_attr

class Student(Person):
    def __init__(self, name, age, student_id):
        super(Student, self).__init__(name, age)
        self.student_id = student_id

student = Student("张三", 20, "2023001")
print(student.name)  # 张三
print(student.age)   # 20
print(student.student_id)  # 2023001
print(student.get_private_attr())  # 私有属性
```

### 5.2 类属性继承
```python
class Animal(object):
    species = "动物"
    count = 0
    
    def __init__(self, name):
        self.name = name
        Animal.count += 1

class Dog(Animal):
    species = "狗"  # 重写类属性
    
    def __init__(self, name, breed):
        super(Dog, self).__init__(name)
        self.breed = breed

class Cat(Animal):
    species = "猫"  # 重写类属性
    
    def __init__(self, name, color):
        super(Cat, self).__init__(name)
        self.color = color

dog = Dog("旺财", "金毛")
cat = Cat("咪咪", "橘色")

print(Animal.species)  # 动物
print(Dog.species)     # 狗
print(Cat.species)     # 猫
print(Animal.count)    # 2（两个实例）
```

## 6. 实际应用示例

### 6.1 图形类继承体系
```python
class Shape(object):
    def __init__(self, color):
        self.color = color
    
    def get_color(self):
        return self.color
    
    def area(self):
        raise NotImplementedError("子类必须实现area方法")
    
    def perimeter(self):
        raise NotImplementedError("子类必须实现perimeter方法")

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super(Rectangle, self).__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, color, radius):
        super(Circle, self).__init__(color)
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# 使用
rect = Rectangle("红色", 5, 3)
circle = Circle("蓝色", 4)

print(f"矩形面积: {rect.area()}, 周长: {rect.perimeter()}")
print(f"圆形面积: {circle.area():.2f}, 周长: {circle.perimeter():.2f}")
```

### 6.2 员工管理系统
```python
class Employee(object):
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
    
    def get_info(self):
        return f"员工: {self.name}, ID: {self.employee_id}, 薪资: {self.salary}"
    
    def calculate_bonus(self):
        return self.salary * 0.1

class Manager(Employee):
    def __init__(self, name, employee_id, salary, department):
        super(Manager, self).__init__(name, employee_id, salary)
        self.department = department
        self.team_size = 0
    
    def add_team_member(self):
        self.team_size += 1
    
    def calculate_bonus(self):  # 重写奖金计算方法
        base_bonus = super(Manager, self).calculate_bonus()
        team_bonus = self.team_size * 1000
        return base_bonus + team_bonus
    
    def get_info(self):  # 重写信息获取方法
        base_info = super(Manager, self).get_info()
        return f"{base_info}, 部门: {self.department}, 团队人数: {self.team_size}"

class Developer(Employee):
    def __init__(self, name, employee_id, salary, programming_language):
        super(Developer, self).__init__(name, employee_id, salary)
        self.programming_language = programming_language
        self.projects_completed = 0
    
    def complete_project(self):
        self.projects_completed += 1
    
    def calculate_bonus(self):  # 重写奖金计算方法
        base_bonus = super(Developer, self).calculate_bonus()
        project_bonus = self.projects_completed * 500
        return base_bonus + project_bonus
    
    def get_info(self):  # 重写信息获取方法
        base_info = super(Developer, self).get_info()
        return f"{base_info}, 编程语言: {self.programming_language}, 完成项目: {self.projects_completed}"

# 使用
manager = Manager("张三", "M001", 15000, "技术部")
developer = Developer("李四", "D001", 12000, "Python")

manager.add_team_member()
manager.add_team_member()
developer.complete_project()
developer.complete_project()
developer.complete_project()

print(manager.get_info())
print(f"经理奖金: {manager.calculate_bonus()}")

print(developer.get_info())
print(f"开发员奖金: {developer.calculate_bonus()}")
```

## 7. 常见错误与注意事项

### 7.1 忘记调用父类初始化方法
```python
# ❌ 错误：忘记调用父类初始化
class Student(Person):
    def __init__(self, name, gender, score):
        self.score = score  # 缺少父类初始化

# ✅ 正确：调用父类初始化
class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score
```

### 7.2 多重继承的复杂性
```python
# ❌ 避免过于复杂的多重继承
class A(object): pass
class B(A): pass
class C(A): pass
class D(B, C): pass
class E(C, B): pass
class F(D, E): pass  # 可能导致MRO问题

# ✅ 使用组合代替复杂的多重继承
class Engine(object):
    def start(self):
        return "引擎启动"

class Car(object):
    def __init__(self):
        self.engine = Engine()  # 组合
    
    def start(self):
        return self.engine.start()
```

### 7.3 方法重写时的参数不匹配
```python
# ❌ 错误：参数不匹配
class Parent(object):
    def method(self, x, y):
        return x + y

class Child(Parent):
    def method(self, x):  # 参数不匹配
        return x * 2

# ✅ 正确：保持参数兼容
class Child(Parent):
    def method(self, x, y=None):
        if y is None:
            return x * 2
        return super(Child, self).method(x, y)
```

## 8. 高级特性

### 8.1 抽象基类
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# 不能直接实例化抽象类
# shape = Shape()  # TypeError

# 可以实例化具体实现
rect = Rectangle(5, 3)
print(rect.area())  # 15
```

### 8.2 混入类（Mixin）
```python
class Flyable(object):
    def fly(self):
        return "飞行中..."

class Swimmable(object):
    def swim(self):
        return "游泳中..."

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super(Duck, self).__init__(name)
    
    def make_sound(self):
        return f"{self.name} 嘎嘎叫"

duck = Duck("小鸭")
print(duck.make_sound())  # 小鸭 嘎嘎叫
print(duck.fly())         # 飞行中...
print(duck.swim())        # 游泳中...
```

## 重要提示

1. **单继承**：一个类只能有一个直接父类
2. **多重继承**：一个类可以有多个父类
3. **super()函数**：用于调用父类方法
4. **方法重写**：子类可以重写父类方法
5. **MRO**：方法解析顺序，决定方法调用顺序
6. **组合优于继承**：复杂情况下使用组合代替继承
7. **抽象基类**：定义接口，强制子类实现特定方法
8. **混入类**：提供特定功能的辅助类

# 你可以在底下的代码编辑器中，输入你的代码。



# 然后，点击按钮，交由AI评论
