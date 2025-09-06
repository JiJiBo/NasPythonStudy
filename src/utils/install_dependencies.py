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

# 导入Python环境管理器
from src.utils.PythonEnvManager import python_env_manager

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
        print(f"使用Python: {python_env_manager.get_python_executable()}")
        
        # 解析包名和索引URL
        parts = package.split()
        package_name = parts[0]
        index_url = None
        
        # 查找--index-url参数
        for i, part in enumerate(parts):
            if part == "--index-url" and i + 1 < len(parts):
                index_url = parts[i + 1]
                break
        
        # 使用Python环境管理器安装
        success = python_env_manager.install_package(package_name, index_url)
        
        if success:
            print(f"✓ {package} 安装成功")
            return True
        else:
            print(f"✗ {package} 安装失败")
            return False
            
    except Exception as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def install_package_with_mirror(package_name):
    """使用国内镜像安装Python包"""
    try:
        print(f"正在使用国内镜像安装 {package_name}...")
        print(f"使用Python: {python_env_manager.get_python_executable()}")
        
        # 使用清华镜像
        mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
        success = python_env_manager.install_package(package_name, mirror_url)
        
        if success:
            print(f"✓ {package_name} 安装成功")
            return True
        else:
            print(f"✗ {package_name} 安装失败")
            return False
    except Exception as e:
        print(f"✗ {package_name} 安装失败: {e}")
        return False

def install_cuda_torch_with_mirror(cuda_version):
    """使用国内镜像安装CUDA版本的PyTorch"""
    try:
        print(f"尝试使用国内镜像安装CUDA {cuda_version}版本的PyTorch...")
        
        # 尝试多个国内镜像源
        mirrors = [
            "https://pypi.tuna.tsinghua.edu.cn/simple",  # 清华镜像
            "https://mirrors.aliyun.com/pypi/simple",     # 阿里云镜像
            "https://pypi.douban.com/simple",             # 豆瓣镜像
            "https://pypi.mirrors.ustc.edu.cn/simple",    # 中科大镜像
        ]
        
        # 根据CUDA版本确定PyTorch版本
        if cuda_version.startswith("12.8") or cuda_version.startswith("12.7") or cuda_version.startswith("12.6"):
            torch_version = "torch==2.5.1+cu121"
            torchvision_version = "torchvision==0.20.1+cu121"
            torchaudio_version = "torchaudio==2.5.1+cu121"
        elif cuda_version.startswith("12.1"):
            torch_version = "torch==2.5.1+cu121"
            torchvision_version = "torchvision==0.20.1+cu121"
            torchaudio_version = "torchaudio==2.5.1+cu121"
        elif cuda_version.startswith("12.0"):
            torch_version = "torch==2.5.1+cu120"
            torchvision_version = "torchvision==0.20.1+cu120"
            torchaudio_version = "torchaudio==2.5.1+cu120"
        elif cuda_version.startswith("11.8"):
            torch_version = "torch==2.5.1+cu118"
            torchvision_version = "torchvision==0.20.1+cu118"
            torchaudio_version = "torchaudio==2.5.1+cu118"
        else:
            print(f"不支持的CUDA版本: {cuda_version}")
            return False
        
        # 尝试每个镜像源
        for mirror_url in mirrors:
            print(f"尝试镜像: {mirror_url}")
            try:
                # 尝试安装torch
                success = python_env_manager.install_package(torch_version, mirror_url)
                if success:
                    print(f"✓ {torch_version} 安装成功")
                    # 安装torchvision
                    success = python_env_manager.install_package(torchvision_version, mirror_url)
                    if success:
                        print(f"✓ {torchvision_version} 安装成功")
                        # 安装torchaudio
                        success = python_env_manager.install_package(torchaudio_version, mirror_url)
                        if success:
                            print(f"✓ {torchaudio_version} 安装成功")
                            return True
                        else:
                            print(f"✗ {torchaudio_version} 安装失败")
                    else:
                        print(f"✗ {torchvision_version} 安装失败")
                else:
                    print(f"✗ {torch_version} 安装失败")
            except Exception as e:
                print(f"镜像 {mirror_url} 安装失败: {e}")
                continue
        
        print("所有国内镜像都无法安装CUDA版本的PyTorch，将使用官方源")
        return False
        
    except Exception as e:
        print(f"使用国内镜像安装CUDA版本PyTorch失败: {e}")
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

def reinstall_torch_cuda(use_mirror=False):
    """重新安装CUDA版本的torch（用于flet环境）"""
    print("=== 重新安装CUDA版本的torch ===")
    print(f"使用Python环境: {python_env_manager.get_python_executable()}")
    
    if use_mirror:
        print("使用国内镜像加速下载...")
    
    # 首先卸载现有的torch
    print("1. 卸载现有的torch...")
    try:
        python_env_manager.uninstall_package("torch")
        python_env_manager.uninstall_package("torchvision")
        python_env_manager.uninstall_package("torchaudio")
        print("✓ 现有torch卸载完成")
    except:
        print("⚠ 卸载现有torch时出现问题，继续安装...")
    
    # 检测CUDA版本
    cuda_version = detect_cuda_version()
    if cuda_version:
        major_minor = ".".join(cuda_version.split(".")[:2])
        print(f"2. 检测到CUDA {major_minor}，安装对应版本...")
        
        # 根据是否使用镜像选择安装方式
        if use_mirror:
            # 首先尝试使用国内镜像安装CUDA版本
            print("尝试使用国内镜像安装CUDA版本的PyTorch...")
            success = install_cuda_torch_with_mirror(major_minor)
            
            # 如果国内镜像失败，回退到官方源
            if not success:
                print("国内镜像安装失败，回退到官方源...")
                if major_minor.startswith("12.8") or major_minor.startswith("12.7") or major_minor.startswith("12.6"):
                    print("安装CUDA 12.1兼容版本的torch...")
                    success = install_package("torch --index-url https://download.pytorch.org/whl/cu121")
                    if success:
                        install_package("torchvision --index-url https://download.pytorch.org/whl/cu121")
                        install_package("torchaudio --index-url https://download.pytorch.org/whl/cu121")
                elif major_minor.startswith("12.1"):
                    print("安装CUDA 12.1版本的torch...")
                    success = install_package("torch --index-url https://download.pytorch.org/whl/cu121")
                    if success:
                        install_package("torchvision --index-url https://download.pytorch.org/whl/cu121")
                        install_package("torchaudio --index-url https://download.pytorch.org/whl/cu121")
                elif major_minor.startswith("12.0"):
                    print("安装CUDA 12.0版本的torch...")
                    success = install_package("torch --index-url https://download.pytorch.org/whl/cu120")
                    if success:
                        install_package("torchvision --index-url https://download.pytorch.org/whl/cu120")
                        install_package("torchaudio --index-url https://download.pytorch.org/whl/cu120")
                elif major_minor.startswith("11.8"):
                    print("安装CUDA 11.8版本的torch...")
                    success = install_package("torch --index-url https://download.pytorch.org/whl/cu118")
                    if success:
                        install_package("torchvision --index-url https://download.pytorch.org/whl/cu118")
                        install_package("torchaudio --index-url https://download.pytorch.org/whl/cu118")
                else:
                    print("安装CPU版本的torch...")
                    success = install_package_with_mirror("torch")
                    if success:
                        install_package_with_mirror("torchvision")
                        install_package_with_mirror("torchaudio")
        else:
            # 使用官方源安装CUDA版本的torch
            if major_minor.startswith("12.8") or major_minor.startswith("12.7") or major_minor.startswith("12.6"):
                print("安装CUDA 12.1兼容版本的torch...")
                success = install_package("torch --index-url https://download.pytorch.org/whl/cu121")
                if success:
                    install_package("torchvision --index-url https://download.pytorch.org/whl/cu121")
                    install_package("torchaudio --index-url https://download.pytorch.org/whl/cu121")
            elif major_minor.startswith("12.1"):
                print("安装CUDA 12.1版本的torch...")
                success = install_package("torch --index-url https://download.pytorch.org/whl/cu121")
                if success:
                    install_package("torchvision --index-url https://download.pytorch.org/whl/cu121")
                    install_package("torchaudio --index-url https://download.pytorch.org/whl/cu121")
            elif major_minor.startswith("12.0"):
                print("安装CUDA 12.0版本的torch...")
                success = install_package("torch --index-url https://download.pytorch.org/whl/cu120")
                if success:
                    install_package("torchvision --index-url https://download.pytorch.org/whl/cu120")
                    install_package("torchaudio --index-url https://download.pytorch.org/whl/cu120")
            elif major_minor.startswith("11.8"):
                print("安装CUDA 11.8版本的torch...")
                success = install_package("torch --index-url https://download.pytorch.org/whl/cu118")
                if success:
                    install_package("torchvision --index-url https://download.pytorch.org/whl/cu118")
                    install_package("torchaudio --index-url https://download.pytorch.org/whl/cu118")
            else:
                print("安装CPU版本的torch...")
                success = install_package("torch --index-url https://download.pytorch.org/whl/cpu")
                if success:
                    install_package("torchvision --index-url https://download.pytorch.org/whl/cpu")
                    install_package("torchaudio --index-url https://download.pytorch.org/whl/cpu")
        
        if success:
            print("3. 验证安装...")
            try:
                # 使用Python环境管理器验证
                result = python_env_manager.run_python_command([
                    "-c", "import torch; print(f'torch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU数量: {torch.cuda.device_count() if torch.cuda.is_available() else 0}')"
                ])
                
                if result.returncode == 0:
                    print("✓ 验证结果:")
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
    else:
        print("❌ 未检测到CUDA，无法安装CUDA版本的torch")
        return False

def main():
    print("开始安装本地模型所需的依赖...")
    
    # 检查命令行参数
    import sys
    use_mirror = "--use-mirror" in sys.argv
    
    if use_mirror:
        print("使用国内镜像加速下载...")
    
    if len(sys.argv) > 1 and "--reinstall-cuda" in sys.argv:
        print("检测到重新安装CUDA参数，开始重新安装...")
        success = reinstall_torch_cuda(use_mirror=use_mirror)
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
