import re
import cn2an

def extract_number(text: str) -> int:
    """
    提取章节/小节名称里的数字（支持阿拉伯数字和中文数字）
    """
    # 阿拉伯数字
    arabic_match = re.search(r"(\d+)", text)
    if arabic_match:
        return int(arabic_match.group(1))

    # 中文数字
    try:
        return cn2an.cn2an(text, "smart")
    except Exception:
        return 0