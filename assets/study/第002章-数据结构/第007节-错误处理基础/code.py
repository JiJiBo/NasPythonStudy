# 练习：错误处理基础

# 1. 安全的类型转换
def safe_int_conversion(value):
    try:
        return int(value)
    except ValueError:
        print(f"无法将 '{value}' 转换为整数")
        return None

# 2. 安全的除法运算
def safe_division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("错误：不能除以零")
        return None
    except TypeError:
        print("错误：参数必须是数字")
        return None

# 3. 安全的列表访问
def safe_list_access(lst, index):
    try:
        return lst[index]
    except IndexError:
        print(f"错误：索引 {index} 超出范围，列表长度为 {len(lst)}")
        return None

# 4. 测试各种错误情况
# 类型转换错误
result1 = safe_int_conversion("abc")
result2 = safe_int_conversion("123")

# 除零错误
result3 = safe_division(10, 0)
result4 = safe_division(10, 2)

# 列表索引错误
numbers = [1, 2, 3, 4, 5]
result5 = safe_list_access(numbers, 10)
result6 = safe_list_access(numbers, 2)

# 5. 输入验证示例
def validate_age(age_str):
    try:
        age = int(age_str)
        if age < 0:
            print("年龄不能为负数")
            return None
        elif age > 150:
            print("年龄不能超过150")
            return None
        else:
            return age
    except ValueError:
        print("请输入有效的数字")
        return None

# 测试年龄验证
test_age1 = validate_age("25")
test_age2 = validate_age("-5")
test_age3 = validate_age("abc")

# 显示所有结果
result1
result2
result3
result4
result5
result6
test_age1
test_age2
test_age3
