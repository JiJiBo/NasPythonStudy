#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用国内镜像安装PyTorch脚本
支持多个国内镜像源
"""

import subprocess
import sys
import os
from pathlib import Path

def get_python_exe():
    """获取Python可执行文件路径"""
    return Path("python_env/python.exe")

def install_torch_with_mirror(mirror_name="tsinghua"):
    """使用指定镜像安装PyTorch"""
    
    # 国内镜像配置
    mirrors = {
        "tsinghua": {
            "name": "清华大学镜像",
            "url": "https://pypi.tuna.tsinghua.edu.cn/simple",
            "torch_url": "https://pypi.tuna.tsinghua.edu.cn/simple"
        },
        "aliyun": {
            "name": "阿里云镜像", 
            "url": "https://mirrors.aliyun.com/pypi/simple",
            "torch_url": "https://mirrors.aliyun.com/pypi/simple"
        },
        "douban": {
            "name": "豆瓣镜像",
            "url": "https://pypi.douban.com/simple", 
            "torch_url": "https://pypi.douban.com/simple"
        },
        "ustc": {
            "name": "中科大镜像",
            "url": "https://pypi.mirrors.ustc.edu.cn/simple",
            "torch_url": "https://pypi.mirrors.ustc.edu.cn/simple"
        },
        "huawei": {
            "name": "华为云镜像",
            "url": "https://repo.huaweicloud.com/repository/pypi/simple",
            "torch_url": "https://repo.huaweicloud.com/repository/pypi/simple"
        }
    }
    
    if mirror_name not in mirrors:
        print(f"❌ 不支持的镜像: {mirror_name}")
        print(f"支持的镜像: {', '.join(mirrors.keys())}")
        return False
    
    mirror = mirrors[mirror_name]
    python_exe = get_python_exe()
    
    if not python_exe.exists():
        print("❌ Python可执行文件不存在")
        return False
    
    print(f"=== 使用{mirror['name']}安装PyTorch ===")
    print(f"镜像地址: {mirror['url']}")
    
    # 检测CUDA版本
    print("\n1. 检测CUDA版本...")
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=cuda_version", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            cuda_version = result.stdout.strip()
            print(f"✅ 检测到CUDA版本: {cuda_version}")
            
            # 根据CUDA版本选择PyTorch版本
            if cuda_version.startswith("12."):
                torch_index = "https://download.pytorch.org/whl/cu121"
                print(f"使用CUDA 12.x版本的PyTorch: {torch_index}")
            elif cuda_version.startswith("11."):
                torch_index = "https://download.pytorch.org/whl/cu118"
                print(f"使用CUDA 11.x版本的PyTorch: {torch_index}")
            else:
                print(f"⚠️ 不支持的CUDA版本: {cuda_version}，将安装CPU版本")
                torch_index = mirror['torch_url']
        else:
            print("⚠️ 未检测到CUDA，将安装CPU版本")
            torch_index = mirror['torch_url']
            
    except Exception as e:
        print(f"⚠️ CUDA检测失败: {e}，将安装CPU版本")
        torch_index = mirror['torch_url']
    
    # 安装PyTorch
    print(f"\n2. 安装PyTorch...")
    print(f"使用索引: {torch_index}")
    
    try:
        # 先升级pip
        print("升级pip...")
        subprocess.run([
            str(python_exe), "-m", "pip", "install", "--upgrade", "pip",
            "-i", mirror['url']
        ], check=True)
        
        # 安装torch
        if "pytorch.org" in torch_index:
            # 使用PyTorch官方索引
            cmd = [
                str(python_exe), "-m", "pip", "install", 
                "torch", "torchvision", "torchaudio",
                "--index-url", torch_index
            ]
        else:
            # 使用国内镜像
            cmd = [
                str(python_exe), "-m", "pip", "install",
                "torch", "torchvision", "torchaudio", 
                "-i", torch_index
            ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True)
        
        print("✅ PyTorch安装成功！")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PyTorch安装失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 安装过程出错: {e}")
        return False
    
    # 测试安装
    print(f"\n3. 测试PyTorch安装...")
    try:
        result = subprocess.run([
            str(python_exe), "-c", 
            "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyTorch测试成功！")
            print(result.stdout)
        else:
            print(f"⚠️ PyTorch测试失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    return True

def install_other_packages():
    """安装其他必要的包"""
    python_exe = get_python_exe()
    mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    
    packages = [
        "transformers",
        "accelerate", 
        "sentencepiece",
        "protobuf",
        "numpy",
        "requests"
    ]
    
    print(f"\n4. 安装其他必要包...")
    print(f"使用镜像: {mirror_url}")
    
    for package in packages:
        try:
            print(f"安装 {package}...")
            subprocess.run([
                str(python_exe), "-m", "pip", "install", package,
                "-i", mirror_url
            ], check=True)
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ {package} 安装失败: {e}")
        except Exception as e:
            print(f"❌ {package} 安装出错: {e}")

def main():
    """主函数"""
    print("PyTorch国内镜像安装工具")
    print("=" * 50)
    
    # 显示可用镜像
    print("可用的国内镜像:")
    print("1. tsinghua - 清华大学镜像 (推荐)")
    print("2. aliyun - 阿里云镜像")
    print("3. douban - 豆瓣镜像")
    print("4. ustc - 中科大镜像")
    print("5. huawei - 华为云镜像")
    
    # 默认使用清华镜像
    mirror_name = "tsinghua"
    print(f"\n使用镜像: {mirror_name}")
    
    # 安装PyTorch
    success = install_torch_with_mirror(mirror_name)
    
    if success:
        # 安装其他包
        install_other_packages()
        
        print("\n" + "=" * 50)
        print("🎉 安装完成！")
        print("现在可以使用独立的Python环境运行本地模型了。")
    else:
        print("\n❌ 安装失败")

if __name__ == "__main__":
    main()
