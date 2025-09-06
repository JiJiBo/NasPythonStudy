#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动PyTorch拖拽安装器
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 添加python_env到Python路径
python_env_path = current_dir
if python_env_path.exists():
    sys.path.insert(0, str(python_env_path))

try:
    import flet as ft
    from torch_drag_installer import main
    
    print("启动PyTorch拖拽安装器...")
    ft.app(target=main)
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装flet库")
    print("运行: pip install flet")
except Exception as e:
    print(f"启动失败: {e}")
