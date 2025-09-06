# ======= 可编辑区域开始 =======

# 练习1：基本导入
# 导入math模块并计算圆的面积（半径=5）
import math
radius = 5
circle_area = 

# 练习2：特定函数导入
# 从datetime模块导入datetime类，获取当前时间
from datetime import datetime
current_time = 

# 练习3：别名导入
# 导入random模块并给它起别名r，生成1到10的随机数
import random as r
random_number = 

# 练习4：条件导入
# 尝试导入json模块，如果成功则解析JSON字符串
json_string = '{"name": "张三", "age": 25}'
try:
    # 请在这里导入json模块
    pass
    parsed_data = 
    name = 
    age = 
except ImportError:
    name = "导入失败"
    age = 0

# 练习5：模块路径检查
# 导入sys模块，获取Python路径列表的长度
import sys
path_count = 

# 练习6：包信息获取
# 导入platform模块，获取Python版本信息
import platform
python_version = 
system_info = 

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "circle_area": 78.53981633974483,
    "current_time": "datetime对象",
    "random_number": "1到10之间的整数",
    "name": "张三",
    "age": 25,
    "path_count": "大于0的整数",
    "python_version": "包含版本信息的字符串",
    "system_info": "包含系统信息的字符串"
}

# 学生答案
student_answer = {
    "circle_area": circle_area,
    "current_time": str(type(current_time)) if 'current_time' in locals() else None,
    "random_number": random_number if 1 <= random_number <= 10 else None,
    "name": name,
    "age": age,
    "path_count": len(sys.path) if 'sys' in locals() else None,
    "python_version": python_version if 'python_version' in locals() else None,
    "system_info": system_info if 'system_info' in locals() else None
}

# 对比答案并输出结果
student_answer == correct_answer
