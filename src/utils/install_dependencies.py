#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装本地模型所需的依赖
根据用户显卡情况安装对应版本的 torch
"""

import subprocess
import sys
import shutil
import os

# 设置输出编码，确保中文正确显示
if sys.platform.startswith('win'):
    # Windows系统设置控制台编码
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

def run_cmd(cmd):
    try:
        # 在Windows上使用cp936编码（GBK），在其他系统使用utf-8
        import platform
        if platform.system().lower() == 'windows':
            encoding = 'cp936'  # Windows中文系统默认编码
        else:
            encoding = 'utf-8'
        
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, encoding=encoding, errors='ignore')
        return result
    except Exception as e:
        print(f"命令执行失败: {e}")
        return ""

def detect_cuda_version():
    """检测 CUDA 版本"""
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        # 首先尝试获取版本信息
        version_output = run_cmd([nvidia_smi, "--version"])
        if version_output and "CUDA Version" in version_output:
            # 从版本信息中提取CUDA版本
            for line in version_output.splitlines():
                if "CUDA Version" in line:
                    # 提取版本号，例如 "CUDA Version: 12.8"
                    parts = line.split("CUDA Version")
                    if len(parts) > 1:
                        version_part = parts[1].strip()
                        # 提取数字部分
                        import re
                        version_match = re.search(r'(\d+\.\d+)', version_part)
                        if version_match:
                            return version_match.group(1)
        
        # 如果版本信息获取失败，尝试查询GPU信息
        try:
            gpu_output = run_cmd([nvidia_smi, "--query-gpu=cuda_version", "--format=csv,noheader"])
            if gpu_output and gpu_output.strip():
                # 取第一行的版本号
                first_line = gpu_output.strip().split('\n')[0]
                if first_line and first_line != "Not Supported":
                    return first_line.strip()
        except:
            pass
    
    return None

def install_package(package):
    """安装Python包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + package.split())
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def install_torch():
    """根据显卡情况安装合适的 torch"""
    cuda_version = detect_cuda_version()
    if cuda_version:
        major_minor = ".".join(cuda_version.split(".")[:2])  # e.g., "12.1"
        print(f"检测到 CUDA {major_minor}，安装对应版本的 torch...")
        # 从 PyTorch 官网对应 CUDA wheel
        if major_minor.startswith("12.8") or major_minor.startswith("12.7") or major_minor.startswith("12.6"):
            return install_package("torch --index-url https://download.pytorch.org/whl/cu121")
        elif major_minor.startswith("12.1"):
            return install_package("torch --index-url https://download.pytorch.org/whl/cu121")
        elif major_minor.startswith("12.0"):
            return install_package("torch --index-url https://download.pytorch.org/whl/cu120")
        elif major_minor.startswith("11.8"):
            return install_package("torch --index-url https://download.pytorch.org/whl/cu118")
        else:
            print("未找到完全匹配的 CUDA 版本，安装 CPU 版本的 torch")
            return install_package("torch --index-url https://download.pytorch.org/whl/cpu")
    else:
        print("未检测到 NVIDIA GPU，安装 CPU 版本的 torch")
        return install_package("torch --index-url https://download.pytorch.org/whl/cpu")

def reinstall_torch_cuda():
    """重新安装CUDA版本的torch（用于flet环境）"""
    print("=== 重新安装CUDA版本的torch ===")
    
    # 首先卸载现有的torch
    print("1. 卸载现有的torch...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "torch", "torchvision", "torchaudio", "-y"])
        print("✓ 现有torch卸载完成")
    except:
        print("⚠ 卸载现有torch时出现问题，继续安装...")
    
    # 检测CUDA版本
    cuda_version = detect_cuda_version()
    if cuda_version:
        major_minor = ".".join(cuda_version.split(".")[:2])
        print(f"2. 检测到CUDA {major_minor}，安装对应版本...")
        
        # 安装CUDA版本的torch
        if major_minor.startswith("12.8") or major_minor.startswith("12.7") or major_minor.startswith("12.6"):
            print("安装CUDA 12.1兼容版本的torch...")
            success = install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        elif major_minor.startswith("12.1"):
            print("安装CUDA 12.1版本的torch...")
            success = install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        elif major_minor.startswith("12.0"):
            print("安装CUDA 12.0版本的torch...")
            success = install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu120")
        elif major_minor.startswith("11.8"):
            print("安装CUDA 11.8版本的torch...")
            success = install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        else:
            print("安装CPU版本的torch...")
            success = install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
        
        if success:
            print("3. 验证安装...")
            try:
                import torch
                print(f"✓ torch版本: {torch.__version__}")
                print(f"✓ CUDA可用: {torch.cuda.is_available()}")
                if torch.cuda.is_available():
                    print(f"✓ CUDA版本: {torch.version.cuda}")
                    print(f"✓ GPU数量: {torch.cuda.device_count()}")
                return True
            except Exception as e:
                print(f"❌ 验证失败: {e}")
                return False
        else:
            print("❌ torch安装失败")
            return False
    else:
        print("❌ 未检测到CUDA，无法安装CUDA版本的torch")
        return False

def main():
    print("开始安装本地模型所需的依赖...")
    
    # 检查命令行参数
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reinstall-cuda":
        print("检测到重新安装CUDA参数，开始重新安装...")
        success = reinstall_torch_cuda()
        if success:
            print("✅ CUDA版本torch重新安装成功！")
        else:
            print("❌ CUDA版本torch重新安装失败")
        return

    # 基础依赖
    basic_packages = ["requests", "tqdm"]

    # 可选依赖
    optional_packages = ["transformers", "flet"]

    print("\n=== 安装基础依赖 ===")
    basic_success = sum(install_package(pkg) for pkg in basic_packages)
    print(f"\n基础依赖安装结果: {basic_success}/{len(basic_packages)} 成功")

    print("\n=== 安装 torch ===")
    torch_success = install_torch()

    print("\n=== 安装其他可选依赖 ===")
    optional_success = sum(install_package(pkg) for pkg in optional_packages)

    print("\n=== 安装完成 ===")
    if basic_success == len(basic_packages):
        print("✓ 基础依赖安装完成，模型下载功能可用")
    else:
        print("✗ 基础依赖安装不完整")

    if torch_success and optional_success == len(optional_packages):
        print("✓ 所有依赖安装完成，本地模型功能完全可用")
    elif torch_success or optional_success > 0:
        print("⚠ 部分依赖安装完成，部分功能可用")
    else:
        print("✗ 可选依赖安装失败，本地模型推理功能不可用")

if __name__ == "__main__":
    main()
