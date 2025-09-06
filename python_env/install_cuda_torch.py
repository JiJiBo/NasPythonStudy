#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUDA版本torch安装脚本
专门用于安装CUDA版本的PyTorch
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

from python_launcher import get_python_executable, install_package, uninstall_package, check_package_installed

def detect_cuda_version():
    """检测CUDA版本"""
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        try:
            # 在Windows上使用cp936编码（GBK），在其他系统使用utf-8
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
            
            if result.returncode == 0 and "CUDA Version" in result.stdout:
                for line in result.stdout.splitlines():
                    if "CUDA Version" in line:
                        parts = line.split("CUDA Version")
                        if len(parts) > 1:
                            version_part = parts[1].strip()
                            import re
                            version_match = re.search(r'(\d+\.\d+)', version_part)
                            if version_match:
                                return version_match.group(1)
        except:
            pass
    
    return None

def install_cuda_torch():
    """安装CUDA版本的torch"""
    print("=== 安装CUDA版本的PyTorch ===")
    
    python_exe = get_python_executable()
    print(f"使用Python: {python_exe}")
    
    # 检测CUDA版本
    cuda_version = detect_cuda_version()
    if not cuda_version:
        print("❌ 未检测到CUDA，无法安装CUDA版本的torch")
        return False
    
    print(f"检测到CUDA版本: {cuda_version}")
    
    # 卸载现有的torch
    print("\n1. 卸载现有的torch...")
    packages_to_remove = ["torch", "torchvision", "torchaudio"]
    for package in packages_to_remove:
        if check_package_installed(package):
            print(f"卸载 {package}...")
            uninstall_package(package)
    
    # 根据CUDA版本选择安装命令
    major_minor = ".".join(cuda_version.split(".")[:2])
    print(f"\n2. 安装CUDA {major_minor} 兼容版本的torch...")
    
    if major_minor.startswith("12.8") or major_minor.startswith("12.7") or major_minor.startswith("12.6"):
        print("安装CUDA 12.1兼容版本...")
        index_url = "https://download.pytorch.org/whl/cu121"
    elif major_minor.startswith("12.1"):
        print("安装CUDA 12.1版本...")
        index_url = "https://download.pytorch.org/whl/cu121"
    elif major_minor.startswith("12.0"):
        print("安装CUDA 12.0版本...")
        index_url = "https://download.pytorch.org/whl/cu120"
    elif major_minor.startswith("11.8"):
        print("安装CUDA 11.8版本...")
        index_url = "https://download.pytorch.org/whl/cu118"
    else:
        print("安装CPU版本...")
        index_url = "https://download.pytorch.org/whl/cpu"
    
    # 安装torch
    packages_to_install = ["torch", "torchvision", "torchaudio"]
    success = True
    
    for package in packages_to_install:
        print(f"\n安装 {package}...")
        if not install_package(package, index_url):
            success = False
            break
    
    if success:
        print("\n3. 验证安装...")
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
                print("✅ 验证结果:")
                print(result.stdout)
                return True
            else:
                print(f"❌ 验证失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return False
    else:
        print("❌ torch安装失败")
        return False

def main():
    """主函数"""
    print("开始安装CUDA版本的PyTorch...")
    print("=" * 50)
    
    success = install_cuda_torch()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 CUDA版本torch安装成功！")
        print("现在PyTorch可以正常使用GPU了！")
    else:
        print("❌ CUDA版本torch安装失败")

if __name__ == "__main__":
    main()
