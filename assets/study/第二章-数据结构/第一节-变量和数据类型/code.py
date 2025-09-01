def add(a, b):
    """
    返回两个数的和

    参数:
        a (int or float): 第一个加数
        b (int or float): 第二个加数

    返回:
        int or float: 两个参数的和
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numeric types.")

    return a + b


# 示例调用
add(1, 2)  # 输出: 3