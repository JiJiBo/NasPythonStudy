#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息检测模块
检测CUDA版本、GPU信息等
"""

import subprocess
import shutil
import platform
import sys
from src.utils.PythonEnvManager import python_env_manager

def run_cmd(cmd):
    """运行命令并返回结果"""
    try:
        # 在Windows上使用cp936编码（GBK），在其他系统使用utf-8
        if platform.system().lower() == 'windows':
            encoding = 'cp936'  # Windows中文系统默认编码
        else:
            encoding = 'utf-8'
        
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, encoding=encoding, errors='ignore')
        return result
    except Exception as e:
        return ""

def detect_cuda_version():
    """检测CUDA版本"""
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

def get_gpu_info():
    """获取GPU信息"""
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return None
    
    try:
        # 获取GPU名称和内存信息
        gpu_output = run_cmd([nvidia_smi, "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"])
        if gpu_output and gpu_output.strip():
            lines = gpu_output.strip().split('\n')
            if lines and lines[0]:
                parts = lines[0].split(', ')
                if len(parts) >= 2:
                    gpu_name = parts[0].strip()
                    memory_mb = int(parts[1].strip())
                    memory_gb = memory_mb / 1024
                    return {
                        'name': gpu_name,
                        'memory_gb': memory_gb
                    }
    except:
        pass
    
    return None

def get_torch_info():
    """获取PyTorch信息"""
    try:
        # 使用Python环境管理器获取torch信息
        env_info = python_env_manager.get_environment_info()
        
        if env_info['torch_installed']:
            # 使用Python环境管理器运行torch检查
            result = python_env_manager.run_python_command([
                "-c", "import torch; print(f'version:{torch.__version__}'); print(f'cuda_available:{torch.cuda.is_available()}'); print(f'cuda_version:{torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'gpu_count:{torch.cuda.device_count() if torch.cuda.is_available() else 0}')"
            ])
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                info = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        if key == 'version':
                            info['version'] = value
                        elif key == 'cuda_available':
                            info['cuda_available'] = value == 'True'
                        elif key == 'cuda_version':
                            info['cuda_version'] = value if value != 'N/A' else None
                        elif key == 'gpu_count':
                            info['gpu_count'] = int(value)
                
                return info
        
        return None
    except Exception as e:
        print(f"获取torch信息时出错: {e}")
        return None

def get_system_info():
    """获取完整的系统信息"""
    # 获取Python环境信息
    env_info = python_env_manager.get_environment_info()
    
    info = {
        'system': platform.system(),
        'python_version': env_info.get('python_version', sys.version.split()[0]),
        'python_executable': env_info.get('python_executable', sys.executable),
        'cuda_version': detect_cuda_version(),
        'gpu_info': get_gpu_info(),
        'torch_info': get_torch_info()
    }
    return info

def format_system_info():
    """格式化系统信息为可读文本"""
    info = get_system_info()
    
    lines = []
    lines.append("=== 系统信息 ===")
    lines.append(f"操作系统: {info['system']}")
    lines.append(f"Python版本: {info['python_version']}")
    lines.append(f"Python路径: {info['python_executable']}")
    
    if info['cuda_version']:
        lines.append(f"CUDA版本: {info['cuda_version']}")
    else:
        lines.append("CUDA版本: 未检测到")
    
    if info['gpu_info']:
        lines.append(f"GPU: {info['gpu_info']['name']}")
        lines.append(f"GPU内存: {info['gpu_info']['memory_gb']:.1f} GB")
    else:
        lines.append("GPU: 未检测到")
    
    if info['torch_info']:
        lines.append(f"PyTorch版本: {info['torch_info']['version']}")
        if info['torch_info']['cuda_available']:
            lines.append("PyTorch CUDA支持: ✅ 可用")
            lines.append(f"PyTorch CUDA版本: {info['torch_info']['cuda_version']}")
            lines.append(f"可用GPU数量: {info['torch_info']['gpu_count']}")
        else:
            lines.append("PyTorch CUDA支持: ❌ 不可用")
    else:
        lines.append("PyTorch: 未安装")
    
    return "\n".join(lines)
