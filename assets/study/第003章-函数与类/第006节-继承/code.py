# ======= 可编辑区域开始 =======

# 练习1：单继承
# 定义父类Person
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"我是 {self.name}，今年 {self.age} 岁"

# 定义子类Student，继承Person
class Student(Person):
    def __init__(self, name, age, student_id):
        # 请完成子类初始化，调用父类初始化方法
        pass
    
    def study(self):
        return f"{self.name} 正在学习"

# 创建Student实例
student = Student("张三", 20, "2023001")
student_intro = 
student_study = 

# 练习2：方法重写
# 定义Animal父类
class Animal(object):
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return "动物发出声音"

# 定义Dog子类，重写make_sound方法
class Dog(Animal):
    def __init__(self, name, breed):
        # 请完成子类初始化
        pass
    
    def make_sound(self):
        # 请重写make_sound方法，返回"{name} 汪汪叫"
        pass

# 创建Dog实例并测试方法重写
dog = Dog("旺财", "金毛")
dog_sound = 

# 练习3：多重继承
# 定义两个父类
class Flyable(object):
    def fly(self):
        return "飞行中..."

class Swimmable(object):
    def swim(self):
        return "游泳中..."

# 定义Duck类，继承Animal、Flyable、Swimmable
class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        # 请完成初始化
        pass
    
    def make_sound(self):
        # 请重写make_sound方法，返回"{name} 嘎嘎叫"
        pass

# 创建Duck实例并测试多重继承
duck = Duck("小鸭")
duck_sound = 
duck_fly = 
duck_swim = 

# 练习4：super()函数的使用
# 定义Vehicle父类
class Vehicle(object):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start(self):
        return f"{self.brand} {self.model} 启动"

# 定义Car子类，使用super()调用父类方法
class Car(Vehicle):
    def __init__(self, brand, model, doors):
        # 请使用super()调用父类初始化方法
        pass
    
    def start(self):
        # 请使用super()调用父类start方法，并添加额外信息
        pass

# 创建Car实例并测试super()的使用
car = Car("丰田", "凯美瑞", 4)
car_start = 

# 练习5：类属性继承
# 定义父类
class Shape(object):
    shape_type = "几何图形"
    count = 0
    
    def __init__(self, name):
        self.name = name
        Shape.count += 1

# 定义子类，重写类属性
class Circle(Shape):
    shape_type = "圆形"  # 重写类属性
    
    def __init__(self, name, radius):
        # 请完成初始化
        pass
        self.radius = radius

# 创建实例并测试类属性继承
circle = Circle("圆1", 5)
shape_type = 
shape_count = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "student_intro": "我是 张三，今年 20 岁",
    "student_study": "张三 正在学习",
    "dog_sound": "旺财 汪汪叫",
    "duck_sound": "小鸭 嘎嘎叫",
    "duck_fly": "飞行中...",
    "duck_swim": "游泳中...",
    "car_start": "丰田 凯美瑞 启动，车门数: 4",
    "shape_type": "圆形",
    "shape_count": 1
}

# 学生答案
student_answer = {
    "student_intro": student_intro,
    "student_study": student_study,
    "dog_sound": dog_sound,
    "duck_sound": duck_sound,
    "duck_fly": duck_fly,
    "duck_swim": duck_swim,
    "car_start": car_start,
    "shape_type": shape_type,
    "shape_count": shape_count
}

# 对比答案并输出结果
student_answer == correct_answer
