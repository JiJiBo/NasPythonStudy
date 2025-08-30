def add(a: str, b: str) -> str:
    """
    拼接两个字符串并返回结果。

    Args:
        a (str): 第一个要拼接的字符串。
        b (str): 第二个要拼接的字符串.

    Returns:
        str: 两个字符串拼接后的结果。
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("Both arguments must be strings.")
    return a + b

# 测试代码
add("a", "b")  # 输出：ab