#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装本地模型所需的依赖
"""

import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def main():
    """主安装函数"""
    print("开始安装本地模型所需的依赖...")
    
    # 基础依赖
    basic_packages = [
        "requests",
        "tqdm",
    ]
    
    # 可选依赖（如果安装失败不会影响基本功能）
    optional_packages = [
        "torch",  # PyTorch - 用于本地模型推理
        "transformers",  # Hugging Face transformers
        "flet",  # UI框架
    ]
    
    print("\n=== 安装基础依赖 ===")
    basic_success = 0
    for package in basic_packages:
        if install_package(package):
            basic_success += 1
    
    print(f"\n基础依赖安装结果: {basic_success}/{len(basic_packages)} 成功")
    
    print("\n=== 安装可选依赖 ===")
    optional_success = 0
    for package in optional_packages:
        if install_package(package):
            optional_success += 1
    
    print(f"\n可选依赖安装结果: {optional_success}/{len(optional_packages)} 成功")
    
    print("\n=== 安装完成 ===")
    if basic_success == len(basic_packages):
        print("✓ 基础依赖安装完成，模型下载功能可用")
    else:
        print("✗ 基础依赖安装不完整")
    
    if optional_success == len(optional_packages):
        print("✓ 所有依赖安装完成，本地模型功能完全可用")
    elif optional_success > 0:
        print("⚠ 部分依赖安装完成，部分功能可用")
    else:
        print("✗ 可选依赖安装失败，本地模型推理功能不可用")
        print("提示: 可以手动安装 torch 和 transformers 来启用本地模型功能")

if __name__ == "__main__":
    main()
