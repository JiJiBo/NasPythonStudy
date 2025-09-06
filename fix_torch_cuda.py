#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复PyTorch CUDA版本问题
"""

import subprocess
import sys
import os

def fix_torch_cuda():
    """修复PyTorch CUDA版本问题"""
    print("=== 修复PyTorch CUDA版本问题 ===")
    
    # 1. 卸载现有的CPU版本torch
    print("1. 卸载现有的CPU版本torch...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "uninstall", 
            "torch", "torchvision", "torchaudio", "-y"
        ])
        print("✅ CPU版本torch卸载完成")
    except Exception as e:
        print(f"⚠️ 卸载时出现问题: {e}")
    
    # 2. 安装CUDA版本torch
    print("\n2. 安装CUDA版本torch...")
    print("检测到CUDA 12.8，安装cu121兼容版本...")
    
    try:
        # 安装CUDA 12.1兼容版本（支持CUDA 12.6-12.8）
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "torch", "torchvision", "torchaudio",
            "--index-url", "https://download.pytorch.org/whl/cu121"
        ])
        print("✅ CUDA版本torch安装完成")
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False
    
    # 3. 验证安装
    print("\n3. 验证安装...")
    try:
        import torch
        print(f"✅ torch版本: {torch.__version__}")
        print(f"✅ CUDA可用: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA版本: {torch.version.cuda}")
            print(f"✅ GPU数量: {torch.cuda.device_count()}")
            
            if torch.cuda.device_count() > 0:
                gpu_name = torch.cuda.get_device_name(0)
                print(f"✅ GPU名称: {gpu_name}")
                
                # 测试GPU计算
                print("\n4. 测试GPU计算...")
                x = torch.randn(3, 3).cuda()
                y = x * 2
                result = y.cpu()
                print(f"✅ GPU计算测试成功: {result[0, 0].item():.4f}")
            
            return True
        else:
            print("❌ CUDA仍然不可用")
            return False
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    """主函数"""
    print("开始修复PyTorch CUDA版本问题...")
    print("=" * 50)
    
    success = fix_torch_cuda()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 修复成功！现在PyTorch可以正常使用GPU了！")
        print("\n现在您可以:")
        print("1. 重新打开应用")
        print("2. 查看系统信息，应该显示CUDA支持可用")
        print("3. 使用本地模型功能")
    else:
        print("❌ 修复失败，请检查错误信息")

if __name__ == "__main__":
    main()
