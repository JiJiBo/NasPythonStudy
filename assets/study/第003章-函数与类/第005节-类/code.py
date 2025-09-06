# ======= 可编辑区域开始 =======

# 练习1：定义类并创建实例
# 定义一个Person类，包含name和age属性
class Person(object):
    def __init__(self, name, age):
        # 请完成初始化方法
        pass

# 创建两个Person实例
person1 = 
person2 = 

# 练习2：添加实例方法
# 为Person类添加一个introduce方法，返回自我介绍
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        # 请完成自我介绍方法，返回格式："我是{name}，今年{age}岁"
        pass

# 创建实例并调用方法
person = Person("张三", 25)
introduction = 

# 练习3：类属性
# 为Person类添加一个类属性species，值为"人类"
class Person(object):
    # 请添加类属性species
    pass
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 访问类属性
species = 

# 练习4：私有属性
# 为Person类添加私有属性__id，并提供getter和setter方法
class Person(object):
    def __init__(self, name, age, person_id):
        self.name = name
        self.age = age
        # 请添加私有属性__id
        pass
    
    def get_id(self):
        # 请完成获取ID的方法
        pass
    
    def set_id(self, new_id):
        # 请完成设置ID的方法
        pass

# 创建实例并测试私有属性
person = Person("李四", 30, "ID001")
person_id = 
person.set_id("ID002")
new_id = 

# 练习5：类方法
# 为Person类添加一个类方法get_species，返回species类属性
class Person(object):
    species = "人类"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @classmethod
    def get_species(cls):
        # 请完成类方法
        pass

# 调用类方法
species_info = 

# 练习6：静态方法
# 为Person类添加一个静态方法is_adult，判断年龄是否大于等于18
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @staticmethod
    def is_adult(age):
        # 请完成静态方法，判断年龄是否大于等于18
        pass

# 调用静态方法
is_adult_result = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "person1_name": "张三",
    "person1_age": 25,
    "person2_name": "李四", 
    "person2_age": 30,
    "introduction": "我是张三，今年25岁",
    "species": "人类",
    "person_id": "ID001",
    "new_id": "ID002",
    "species_info": "人类",
    "is_adult_result": True
}

# 学生答案
student_answer = {
    "person1_name": person1.name if hasattr(person1, 'name') else None,
    "person1_age": person1.age if hasattr(person1, 'age') else None,
    "person2_name": person2.name if hasattr(person2, 'name') else None,
    "person2_age": person2.age if hasattr(person2, 'age') else None,
    "introduction": introduction,
    "species": species,
    "person_id": person_id,
    "new_id": new_id,
    "species_info": species_info,
    "is_adult_result": is_adult_result
}

# 对比答案并输出结果
student_answer == correct_answer
