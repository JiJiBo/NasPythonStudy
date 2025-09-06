#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python环境管理器
管理集成的Python环境和CUDA升级
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

class PythonEnvManager:
    def __init__(self, app_root_dir=None):
        """
        初始化Python环境管理器
        
        Args:
            app_root_dir: 应用根目录，如果为None则自动检测
        """
        if app_root_dir is None:
            # 自动检测应用根目录
            current_file = Path(__file__).resolve()
            app_root_dir = current_file.parent.parent.parent
        
        self.app_root = Path(app_root_dir)
        self.python_dir = self.app_root / "python_env"
        self.python_exe = None
        self.pip_exe = None
        
        # 初始化Python环境
        self._init_python_env()
    
    def _init_python_env(self):
        """初始化Python环境"""
        # 创建Python环境目录
        self.python_dir.mkdir(exist_ok=True)
        
        # 检测Python可执行文件
        if platform.system().lower() == 'windows':
            python_exe_name = "python.exe"
            pip_exe_name = "pip.exe"
        else:
            python_exe_name = "python"
            pip_exe_name = "pip"
        
        # 查找Python可执行文件
        self.python_exe = self._find_python_executable()
        if self.python_exe:
            # 查找对应的pip
            python_dir = Path(self.python_exe).parent
            self.pip_exe = python_dir / pip_exe_name
            
            # 如果pip不存在，尝试使用python -m pip
            if not self.pip_exe.exists():
                self.pip_exe = None
    
    def _find_python_executable(self):
        """查找Python可执行文件"""
        # 优先级顺序：
        # 1. 当前Python解释器
        # 2. 系统PATH中的python
        # 3. conda环境中的python
        
        # 1. 使用当前Python解释器
        current_python = sys.executable
        if current_python and Path(current_python).exists():
            return current_python
        
        # 2. 查找系统PATH中的python
        python_candidates = ["python", "python3", "python.exe", "python3.exe"]
        for candidate in python_candidates:
            python_path = shutil.which(candidate)
            if python_path:
                return python_path
        
        return None
    
    def get_python_executable(self):
        """获取Python可执行文件路径"""
        return self.python_exe
    
    def get_pip_executable(self):
        """获取pip可执行文件路径"""
        return self.pip_exe
    
    def run_python_command(self, args, cwd=None, env=None):
        """
        运行Python命令
        
        Args:
            args: 命令参数列表
            cwd: 工作目录
            env: 环境变量
            
        Returns:
            subprocess.CompletedProcess对象
        """
        if not self.python_exe:
            raise RuntimeError("Python可执行文件未找到")
        
        cmd = [self.python_exe] + args
        
        # 设置环境变量
        if env is None:
            env = os.environ.copy()
        
        # 确保UTF-8编码
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
    
    def run_pip_command(self, args, cwd=None, env=None):
        """
        运行pip命令
        
        Args:
            args: 命令参数列表
            cwd: 工作目录
            env: 环境变量
            
        Returns:
            subprocess.CompletedProcess对象
        """
        if self.pip_exe and self.pip_exe.exists():
            cmd = [str(self.pip_exe)] + args
        else:
            # 使用python -m pip
            cmd = [self.python_exe, "-m", "pip"] + args
        
        # 设置环境变量
        if env is None:
            env = os.environ.copy()
        
        # 确保UTF-8编码
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
    
    def install_package(self, package_name, index_url=None):
        """
        安装Python包
        
        Args:
            package_name: 包名
            index_url: 索引URL
            
        Returns:
            bool: 安装是否成功
        """
        try:
            args = ["install", package_name]
            if index_url:
                args.extend(["--index-url", index_url])
            
            result = self.run_pip_command(args)
            
            if result.returncode == 0:
                print(f"✅ {package_name} 安装成功")
                return True
            else:
                print(f"❌ {package_name} 安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 安装 {package_name} 时出错: {e}")
            return False
    
    def uninstall_package(self, package_name):
        """
        卸载Python包
        
        Args:
            package_name: 包名
            
        Returns:
            bool: 卸载是否成功
        """
        try:
            args = ["uninstall", package_name, "-y"]
            result = self.run_pip_command(args)
            
            if result.returncode == 0:
                print(f"✅ {package_name} 卸载成功")
                return True
            else:
                print(f"❌ {package_name} 卸载失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 卸载 {package_name} 时出错: {e}")
            return False
    
    def check_package_installed(self, package_name):
        """
        检查包是否已安装
        
        Args:
            package_name: 包名
            
        Returns:
            bool: 是否已安装
        """
        try:
            result = self.run_pip_command(["show", package_name])
            return result.returncode == 0
        except:
            return False
    
    def get_package_version(self, package_name):
        """
        获取包版本
        
        Args:
            package_name: 包名
            
        Returns:
            str: 版本号，如果未安装返回None
        """
        try:
            result = self.run_pip_command(["show", package_name])
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        return line.split(':', 1)[1].strip()
            return None
        except:
            return None
    
    def get_environment_info(self):
        """
        获取环境信息
        
        Returns:
            dict: 环境信息
        """
        info = {
            'python_executable': self.python_exe,
            'pip_executable': self.pip_exe,
            'python_version': None,
            'torch_installed': False,
            'torch_version': None,
            'cuda_available': False
        }
        
        if self.python_exe:
            try:
                # 获取Python版本
                result = self.run_python_command(["--version"])
                if result.returncode == 0:
                    info['python_version'] = result.stdout.strip()
                
                # 检查torch
                if self.check_package_installed('torch'):
                    info['torch_installed'] = True
                    info['torch_version'] = self.get_package_version('torch')
                    
                    # 检查CUDA可用性
                    try:
                        result = self.run_python_command([
                            "-c", "import torch; print(torch.cuda.is_available())"
                        ])
                        if result.returncode == 0:
                            info['cuda_available'] = result.stdout.strip() == "True"
                    except:
                        pass
                        
            except Exception as e:
                print(f"获取环境信息时出错: {e}")
        
        return info

# 全局Python环境管理器实例
python_env_manager = PythonEnvManager()
