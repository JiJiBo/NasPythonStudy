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
import time
from src.utils.PythonEnvManager import python_env_manager

# 缓存系统信息，避免重复检测
_system_info_cache = {}
_cache_timestamp = 0
_cache_duration = 30  # 缓存30秒

def clear_system_info_cache():
    """清除系统信息缓存，强制重新检测"""
    global _system_info_cache, _cache_timestamp
    _system_info_cache.clear()
    _cache_timestamp = 0

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
    global _system_info_cache, _cache_timestamp
    
    # 检查缓存
    current_time = time.time()
    if 'cuda_version' in _system_info_cache and (current_time - _cache_timestamp) < _cache_duration:
        return _system_info_cache['cuda_version']
    
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
                            cuda_version = version_match.group(1)
                            # 缓存结果
                            _system_info_cache['cuda_version'] = cuda_version
                            _cache_timestamp = current_time
                            return cuda_version
        
        # 如果版本信息获取失败，尝试查询GPU信息
        try:
            gpu_output = run_cmd([nvidia_smi, "--query-gpu=cuda_version", "--format=csv,noheader"])
            if gpu_output and gpu_output.strip():
                # 取第一行的版本号
                first_line = gpu_output.strip().split('\n')[0]
                if first_line and first_line != "Not Supported":
                    cuda_version = first_line.strip()
                    # 缓存结果
                    _system_info_cache['cuda_version'] = cuda_version
                    _cache_timestamp = current_time
                    return cuda_version
        except:
            pass
    
    # 缓存None结果
    _system_info_cache['cuda_version'] = None
    _cache_timestamp = current_time
    return None

def get_gpu_info():
    """获取GPU信息"""
    global _system_info_cache, _cache_timestamp
    
    # 检查缓存
    current_time = time.time()
    if 'gpu_info' in _system_info_cache and (current_time - _cache_timestamp) < _cache_duration:
        return _system_info_cache['gpu_info']
    
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        # 缓存None结果
        _system_info_cache['gpu_info'] = None
        _cache_timestamp = current_time
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
                    gpu_info = {
                        'name': gpu_name,
                        'memory_gb': memory_gb
                    }
                    # 缓存结果
                    _system_info_cache['gpu_info'] = gpu_info
                    _cache_timestamp = current_time
                    return gpu_info
    except:
        pass
    
    # 缓存None结果
    _system_info_cache['gpu_info'] = None
    _cache_timestamp = current_time
    return None

def get_torch_info():
    """获取PyTorch信息"""
    global _system_info_cache, _cache_timestamp
    
    # 检查缓存
    current_time = time.time()
    if 'torch_info' in _system_info_cache and (current_time - _cache_timestamp) < _cache_duration:
        return _system_info_cache['torch_info']
    
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
                
                # 缓存结果
                _system_info_cache['torch_info'] = info
                _cache_timestamp = current_time
                return info
        
        # 缓存None结果
        _system_info_cache['torch_info'] = None
        _cache_timestamp = current_time
        return None
    except Exception as e:
        print(f"获取torch信息时出错: {e}")
        # 缓存None结果
        _system_info_cache['torch_info'] = None
        _cache_timestamp = current_time
        return None

def get_system_info():
    """获取完整的系统信息"""
    # 获取Python环境信息
    env_info = python_env_manager.get_environment_info()
    
    # 获取虚拟环境信息
    virtual_env_info = get_virtual_env_info()
    
    info = {
        'system': platform.system(),
        'python_version': env_info.get('python_version', sys.version.split()[0]),
        'python_executable': env_info.get('python_executable', sys.executable),
        'virtual_env': virtual_env_info,
        'cuda_version': detect_cuda_version(),
        'gpu_info': get_gpu_info(),
        'torch_info': get_torch_info()
    }
    return info

def get_virtual_env_info():
    """获取虚拟环境信息"""
    try:
        from pathlib import Path
        
        # 检查python_env目录
        python_env_path = Path("python_env")
        if not python_env_path.exists():
            return {
                'exists': False,
                'path': None,
                'python_exe': None,
                'pip_exe': None,
                'packages': []
            }
        
        # 获取Python可执行文件路径
        python_exe = python_env_path / "python.exe"
        pip_exe = python_env_path / "Scripts" / "pip.exe"
        
        # 获取已安装的包
        packages = []
        if python_exe.exists():
            try:
                result = subprocess.run(
                    [str(python_exe), "-m", "pip", "list", "--format=freeze"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        if line and '==' in line:
                            package_name = line.split('==')[0]
                            if package_name.lower() in ['torch', 'torchvision', 'torchaudio', 'transformers', 'flet']:
                                packages.append(line)
            except:
                pass
        
        return {
            'exists': True,
            'path': str(python_env_path.absolute()),
            'python_exe': str(python_exe.absolute()) if python_exe.exists() else None,
            'pip_exe': str(pip_exe.absolute()) if pip_exe.exists() else None,
            'packages': packages
        }
    except Exception as e:
        return {
            'exists': False,
            'error': str(e)
        }

def format_system_info():
    """格式化系统信息为可读文本"""
    info = get_system_info()
    
    lines = []
    lines.append("=== 系统信息 ===")
    lines.append(f"操作系统: {info['system']}")
    lines.append(f"Python版本: {info['python_version']}")
    lines.append(f"Python路径: {info['python_executable']}")
    
    # 虚拟环境信息
    lines.append("\n=== 虚拟环境信息 ===")
    virtual_env = info['virtual_env']
    if virtual_env['exists']:
        lines.append("✅ 虚拟环境: 已创建")
        lines.append(f"虚拟环境路径: {virtual_env['path']}")
        if virtual_env['python_exe']:
            lines.append(f"Python可执行文件: {virtual_env['python_exe']}")
        if virtual_env['pip_exe']:
            lines.append(f"pip可执行文件: {virtual_env['pip_exe']}")
        
        if virtual_env['packages']:
            lines.append("\n已安装的关键包:")
            for package in virtual_env['packages']:
                lines.append(f"  • {package}")
        else:
            lines.append("已安装的关键包: 无")
    else:
        lines.append("❌ 虚拟环境: 未创建")
        if 'error' in virtual_env:
            lines.append(f"错误: {virtual_env['error']}")
    
    # CUDA和GPU信息
    lines.append("\n=== GPU信息 ===")
    if info['cuda_version']:
        lines.append(f"CUDA版本: {info['cuda_version']}")
    else:
        lines.append("CUDA版本: 未检测到")
    
    if info['gpu_info']:
        lines.append(f"GPU: {info['gpu_info']['name']}")
        lines.append(f"GPU内存: {info['gpu_info']['memory_gb']:.1f} GB")
    else:
        lines.append("GPU: 未检测到")
    
    # PyTorch信息
    lines.append("\n=== PyTorch信息 ===")
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
