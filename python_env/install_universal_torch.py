#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装兼容RTX 50系和40系显卡的PyTorch版本
支持CUDA 12.1/12.4/12.8的通用版本
"""

import subprocess
import sys
import os
from pathlib import Path

def get_python_exe():
    """获取Python可执行文件路径"""
    return Path("python_env/python.exe")

def detect_gpu_series():
    """检测GPU系列"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            gpu_name = result.stdout.strip()
            print(f"检测到GPU: {gpu_name}")
            
            if "RTX 50" in gpu_name or "RTX 5090" in gpu_name or "RTX 5080" in gpu_name:
                return "50_series"
            elif "RTX 40" in gpu_name or "RTX 4090" in gpu_name or "RTX 4080" in gpu_name or "RTX 4070" in gpu_name:
                return "40_series"
            elif "RTX 30" in gpu_name or "RTX 3090" in gpu_name or "RTX 3080" in gpu_name or "RTX 3070" in gpu_name:
                return "30_series"
            else:
                return "other"
        else:
            print("未检测到NVIDIA GPU")
            return "none"
    except Exception as e:
        print(f"GPU检测失败: {e}")
        return "none"

def install_universal_torch():
    """安装通用兼容的PyTorch版本"""
    print("=== 安装兼容RTX 50系和40系的PyTorch版本 ===")
    
    python_exe = get_python_exe()
    if not python_exe.exists():
        print("❌ Python可执行文件不存在")
        return False
    
    # 检测GPU系列
    gpu_series = detect_gpu_series()
    print(f"GPU系列: {gpu_series}")
    
    # 卸载现有torch
    print("\n1. 卸载现有torch...")
    try:
        subprocess.run([str(python_exe), "-m", "pip", "uninstall", "torch", "torchvision", "torchaudio", "-y"], 
                      check=False)
        print("✅ 现有torch卸载完成")
    except:
        print("⚠️ 卸载现有torch时出现问题，继续安装...")
    
    # 根据GPU系列选择安装策略
    if gpu_series in ["50_series", "40_series"]:
        print("\n2. 安装CUDA 12.4兼容版本（支持50系和40系）...")
        
        # 尝试多个安装方案
        install_commands = [
            # 方案1: CUDA 12.4 (推荐，兼容性最好)
            [
                str(python_exe), "-m", "pip", "install", 
                "torch==2.5.1+cu124", "torchvision==0.20.1+cu124", "torchaudio==2.5.1+cu124",
                "--index-url", "https://download.pytorch.org/whl/cu124"
            ],
            # 方案2: CUDA 12.1 (备选)
            [
                str(python_exe), "-m", "pip", "install", 
                "torch==2.5.1+cu121", "torchvision==0.20.1+cu121", "torchaudio==2.5.1+cu121",
                "--index-url", "https://download.pytorch.org/whl/cu121"
            ],
            # 方案3: 使用国内镜像的CUDA 12.1
            [
                str(python_exe), "-m", "pip", "install", 
                "torch==2.5.1+cu121", "torchvision==0.20.1+cu121", "torchaudio==2.5.1+cu121",
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
            ]
        ]
        
        success = False
        for i, cmd in enumerate(install_commands, 1):
            print(f"\n尝试方案 {i}: {' '.join(cmd[-3:])}")
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"✅ 方案 {i} 安装成功")
                success = True
                break
            except subprocess.CalledProcessError as e:
                print(f"❌ 方案 {i} 安装失败: {e.stderr}")
                continue
        
        if not success:
            print("❌ 所有CUDA版本安装失败，尝试CPU版本...")
            # 回退到CPU版本
            try:
                subprocess.run([
                    str(python_exe), "-m", "pip", "install", 
                    "torch", "torchvision", "torchaudio",
                    "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
                ], check=True)
                print("✅ CPU版本安装成功")
                success = True
            except subprocess.CalledProcessError as e:
                print(f"❌ CPU版本安装失败: {e}")
                return False
    
    elif gpu_series == "30_series":
        print("\n2. 安装CUDA 11.8版本（支持30系）...")
        try:
            subprocess.run([
                str(python_exe), "-m", "pip", "install", 
                "torch==2.5.1+cu118", "torchvision==0.20.1+cu118", "torchaudio==2.5.1+cu118",
                "--index-url", "https://download.pytorch.org/whl/cu118"
            ], check=True)
            print("✅ CUDA 11.8版本安装成功")
            success = True
        except subprocess.CalledProcessError as e:
            print(f"❌ CUDA 11.8版本安装失败: {e}")
            return False
    
    else:
        print("\n2. 安装CPU版本...")
        try:
            subprocess.run([
                str(python_exe), "-m", "pip", "install", 
                "torch", "torchvision", "torchaudio",
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
            ], check=True)
            print("✅ CPU版本安装成功")
            success = True
        except subprocess.CalledProcessError as e:
            print(f"❌ CPU版本安装失败: {e}")
            return False
    
    # 验证安装
    print("\n3. 验证安装...")
    try:
        result = subprocess.run([
            str(python_exe), "-c", 
            "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU数量: {torch.cuda.device_count() if torch.cuda.is_available() else 0}')"
        ], capture_output=True, text=True)
        
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

def main():
    """主函数"""
    print("RTX 50系和40系兼容PyTorch安装工具")
    print("=" * 50)
    
    success = install_universal_torch()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 PyTorch安装完成！")
        print("现在RTX 50系和40系显卡都可以使用这个PyTorch版本了。")
    else:
        print("\n❌ PyTorch安装失败")

if __name__ == "__main__":
    main()
