#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立启动PyTorch版本选择器
避免DLL冲突问题
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """主函数"""
    try:
        # 获取当前脚本目录
        current_dir = Path(__file__).parent
        script_path = current_dir / "torch_version_selector.py"
        
        # 使用独立的Python进程启动
        python_exe = current_dir / "python.exe"
        
        if not python_exe.exists():
            print("❌ Python可执行文件不存在")
            return
        
        if not script_path.exists():
            print("❌ PyTorch版本选择器脚本不存在")
            return
        
        print("🚀 启动PyTorch版本选择器...")
        print(f"Python路径: {python_exe}")
        print(f"脚本路径: {script_path}")
        
        # 启动独立的Python进程
        subprocess.Popen([
            str(python_exe),
            str(script_path)
        ])
        
        print("✅ PyTorch版本选择器已启动")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
