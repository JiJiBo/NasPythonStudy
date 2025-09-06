#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python环境启动器
用于在flet应用中启动Python环境
"""

import sys
import os
import subprocess
from pathlib import Path

def get_python_executable():
    """获取Python可执行文件路径"""
    # 优先级顺序：
    # 1. 当前Python解释器
    # 2. 系统PATH中的python
    # 3. conda环境中的python
    
    # 1. 使用当前Python解释器
    current_python = sys.executable
    if current_python and Path(current_python).exists():
        return current_python
    
    # 2. 查找系统PATH中的python
    import shutil
    python_candidates = ["python", "python3", "python.exe", "python3.exe"]
    for candidate in python_candidates:
        python_path = shutil.which(candidate)
        if python_path:
            return python_path
    
    return None

def run_python_script(script_path, args=None, cwd=None):
    """
    运行Python脚本
    
    Args:
        script_path: 脚本路径
        args: 脚本参数
        cwd: 工作目录
        
    Returns:
        subprocess.CompletedProcess对象
    """
    python_exe = get_python_executable()
    if not python_exe:
        raise RuntimeError("Python可执行文件未找到")
    
    cmd = [python_exe, script_path]
    if args:
        cmd.extend(args)
    
    # 设置环境变量
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

def install_package(package_name, index_url=None):
    """
    安装Python包
    
    Args:
        package_name: 包名
        index_url: 索引URL
        
    Returns:
        bool: 安装是否成功
    """
    python_exe = get_python_executable()
    if not python_exe:
        raise RuntimeError("Python可执行文件未找到")
    
    cmd = [python_exe, "-m", "pip", "install", package_name]
    if index_url:
        cmd.extend(["--index-url", index_url])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print(f"✅ {package_name} 安装成功")
            return True
        else:
            print(f"❌ {package_name} 安装失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装 {package_name} 时出错: {e}")
        return False

def uninstall_package(package_name):
    """
    卸载Python包
    
    Args:
        package_name: 包名
        
    Returns:
        bool: 卸载是否成功
    """
    python_exe = get_python_executable()
    if not python_exe:
        raise RuntimeError("Python可执行文件未找到")
    
    cmd = [python_exe, "-m", "pip", "uninstall", package_name, "-y"]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print(f"✅ {package_name} 卸载成功")
            return True
        else:
            print(f"❌ {package_name} 卸载失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 卸载 {package_name} 时出错: {e}")
        return False

def check_package_installed(package_name):
    """
    检查包是否已安装
    
    Args:
        package_name: 包名
        
    Returns:
        bool: 是否已安装
    """
    python_exe = get_python_executable()
    if not python_exe:
        return False
    
    cmd = [python_exe, "-m", "pip", "show", package_name]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode == 0
    except:
        return False

def get_package_version(package_name):
    """
    获取包版本
    
    Args:
        package_name: 包名
        
    Returns:
        str: 版本号，如果未安装返回None
    """
    python_exe = get_python_executable()
    if not python_exe:
        return None
    
    cmd = [python_exe, "-m", "pip", "show", package_name]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
        return None
    except:
        return None

def get_environment_info():
    """
    获取环境信息
    
    Returns:
        dict: 环境信息
    """
    info = {
        'python_executable': get_python_executable(),
        'python_version': None,
        'torch_installed': False,
        'torch_version': None,
        'cuda_available': False
    }
    
    python_exe = get_python_executable()
    if python_exe:
        try:
            # 获取Python版本
            result = subprocess.run(
                [python_exe, "--version"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                info['python_version'] = result.stdout.strip()
            
            # 检查torch
            if check_package_installed('torch'):
                info['torch_installed'] = True
                info['torch_version'] = get_package_version('torch')
                
                # 检查CUDA可用性
                try:
                    result = subprocess.run(
                        [python_exe, "-c", "import torch; print(torch.cuda.is_available())"],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    if result.returncode == 0:
                        info['cuda_available'] = result.stdout.strip() == "True"
                except:
                    pass
                    
        except Exception as e:
            print(f"获取环境信息时出错: {e}")
    
    return info

if __name__ == "__main__":
    # 测试功能
    print("=== Python环境启动器测试 ===")
    
    info = get_environment_info()
    print(f"Python可执行文件: {info['python_executable']}")
    print(f"Python版本: {info['python_version']}")
    print(f"torch已安装: {info['torch_installed']}")
    print(f"torch版本: {info['torch_version']}")
    print(f"CUDA可用: {info['cuda_available']}")
