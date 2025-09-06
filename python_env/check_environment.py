#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本
检查Python环境和CUDA支持状态
"""

import sys
import os
import subprocess
import shutil
import platform
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from python_launcher import get_python_executable, get_environment_info, check_package_installed, get_package_version

def check_system_info():
    """检查系统信息"""
    print("=== 系统信息 ===")
    print(f"操作系统: {platform.system()}")
    print(f"Python可执行文件: {get_python_executable()}")
    
    # 获取环境信息
    env_info = get_environment_info()
    print(f"Python版本: {env_info.get('python_version', 'Unknown')}")
    print(f"torch已安装: {env_info.get('torch_installed', False)}")
    print(f"torch版本: {env_info.get('torch_version', 'N/A')}")
    print(f"CUDA可用: {env_info.get('cuda_available', False)}")

def check_cuda_info():
    """检查CUDA信息"""
    print("\n=== CUDA信息 ===")
    
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        print(f"nvidia-smi路径: {nvidia_smi}")
        
        try:
            # 获取CUDA版本
            if platform.system().lower() == 'windows':
                encoding = 'cp936'
            else:
                encoding = 'utf-8'
            
            result = subprocess.run(
                [nvidia_smi, "--version"],
                capture_output=True,
                text=True,
                encoding=encoding,
                errors='ignore'
            )
            
            if result.returncode == 0:
                print("nvidia-smi输出:")
                print(result.stdout)
            else:
                print(f"nvidia-smi执行失败: {result.stderr}")
                
        except Exception as e:
            print(f"获取CUDA信息时出错: {e}")
    else:
        print("❌ nvidia-smi未找到，可能没有安装NVIDIA驱动")

def check_torch_info():
    """检查torch信息"""
    print("\n=== PyTorch信息 ===")
    
    if check_package_installed('torch'):
        version = get_package_version('torch')
        print(f"torch版本: {version}")
        
        # 检查torch详细信息
        python_exe = get_python_executable()
        if python_exe:
            try:
                result = subprocess.run(
                    [python_exe, "-c", """
import torch
print(f'torch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA版本: {torch.version.cuda}')
    print(f'GPU数量: {torch.cuda.device_count()}')
    if torch.cuda.device_count() > 0:
        print(f'GPU名称: {torch.cuda.get_device_name(0)}')
        
        # 测试GPU计算
        print('测试GPU计算...')
        x = torch.randn(3, 3).cuda()
        y = x * 2
        result = y.cpu()
        print(f'GPU计算测试成功: {result[0, 0].item():.4f}')
else:
    print('CUDA不可用')
                    """],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if result.returncode == 0:
                    print("torch详细信息:")
                    print(result.stdout)
                else:
                    print(f"获取torch信息失败: {result.stderr}")
                    
            except Exception as e:
                print(f"获取torch信息时出错: {e}")
    else:
        print("❌ torch未安装")

def check_other_packages():
    """检查其他重要包"""
    print("\n=== 其他包信息 ===")
    
    packages = ['transformers', 'requests', 'tqdm']
    for package in packages:
        if check_package_installed(package):
            version = get_package_version(package)
            print(f"✅ {package}: {version}")
        else:
            print(f"❌ {package}: 未安装")

def main():
    """主函数"""
    print("开始检查Python环境...")
    print("=" * 60)
    
    check_system_info()
    check_cuda_info()
    check_torch_info()
    check_other_packages()
    
    print("\n" + "=" * 60)
    print("环境检查完成！")

if __name__ == "__main__":
    main()
