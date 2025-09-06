#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python启动器 - 版本 3.11.9
"""

import sys
import os
from pathlib import Path

# 设置Python路径
python_dir = Path(__file__).parent
sys.path.insert(0, str(python_dir))

# 设置环境变量
os.environ['PYTHONPATH'] = str(python_dir)
os.environ['PYTHONIOENCODING'] = 'utf-8'

if __name__ == "__main__":
    print("Python 3.11.9 启动器")
    print(f"Python目录: {python_dir}")
    print(f"Python版本: {sys.version}")
    
    # 测试导入
    try:
        import sys
        print(f"Python可执行文件: {sys.executable}")
    except Exception as e:
        print(f"导入测试失败: {e}")
