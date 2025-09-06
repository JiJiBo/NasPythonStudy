
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的Python环境设置脚本
不依赖外部库
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

def setup_python_environment():
    """设置Python环境"""
    print("=== 设置Python环境 ===")
    
    # 目标目录
    target_dir = Path("python_env")
    python_exe = target_dir / "python.exe"
    
    if not python_exe.exists():
        print("❌ Python可执行文件不存在")
        return False
    
    print(f"✅ Python可执行文件存在: {python_exe}")
    
    # 1. 安装pip
    print("\n1. 正在安装pip...")
    try:
        # 下载get-pip.py
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = target_dir / "get-pip.py"
        
        print(f"正在下载: {get_pip_url}")
        urllib.request.urlretrieve(get_pip_url, get_pip_path)
        print("✅ get-pip.py下载完成")
        
        # 安装pip
        result = subprocess.run(
            [str(python_exe), str(get_pip_path)],
            capture_output=True,
            text=True,
            cwd=str(target_dir)
        )
        
        if result.returncode == 0:
            print("✅ pip安装成功")
        else:
            print(f"⚠️ pip安装可能有问题: {result.stderr}")
        
    except Exception as e:
        print(f"❌ pip安装失败: {e}")
    
    # 2. 创建启动脚本
    print("\n2. 正在创建启动脚本...")
    try:
        launcher_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python启动器 - 版本 3.11.9
"""

import sys
import os
from pathlib import Path

# 设置Python路径
python_dir = Path(__file__).parent
sys.path.insert(0, str(python_dir))

# 设置环境变量
os.environ['PYTHONPATH'] = str(python_dir)
os.environ['PYTHONIOENCODING'] = 'utf-8'

if __name__ == "__main__":
    print("Python 3.11.9 启动器")
    print(f"Python目录: {python_dir}")
    print(f"Python版本: {sys.version}")
    
    # 测试导入
    try:
        import sys
        print(f"Python可执行文件: {sys.executable}")
    except Exception as e:
        print(f"导入测试失败: {e}")
'''
        
        launcher_path = target_dir / "launcher.py"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print("✅ 启动脚本创建完成")
        
    except Exception as e:
        print(f"❌ 创建启动脚本失败: {e}")
    
    # 3. 创建环境信息文件
    print("\n3. 正在创建环境信息文件...")
    try:
        env_info_content = '''# Python环境信息
PYTHON_VERSION=3.11.9
PYTHON_EXECUTABLE=python.exe
PYTHON_DIR=python_env
PLATFORM=Windows
ARCHITECTURE=amd64
'''
        
        env_info_path = target_dir / "env_info.txt"
        with open(env_info_path, 'w', encoding='utf-8') as f:
            f.write(env_info_content)
        
        print("✅ 环境信息文件创建完成")
        
    except Exception as e:
        print(f"❌ 创建环境信息文件失败: {e}")
    
    # 4. 清理下载文件
    print("\n4. 正在清理下载文件...")
    try:
        zip_file = target_dir / "python-3.11.9-embed-amd64.zip"
        if zip_file.exists():
            zip_file.unlink()
            print("✅ 清理zip文件完成")
        
        get_pip_file = target_dir / "get-pip.py"
        if get_pip_file.exists():
            get_pip_file.unlink()
            print("✅ 清理get-pip.py完成")
        
    except Exception as e:
        print(f"⚠️ 清理文件失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Python环境设置完成！")
    print(f"Python路径: {python_exe}")
    print(f"版本: 3.11.9")
    print(f"目录: {target_dir}")
    
    return True

def test_python_installation():
    """测试Python安装"""
    print("\n=== 测试Python安装 ===")
    
    target_dir = Path("python_env")
    python_exe = target_dir / "python.exe"
    
    if not python_exe.exists():
        print("❌ Python可执行文件不存在")
        return False
    
    try:
        # 测试Python版本
        result = subprocess.run(
            [str(python_exe), "--version"],
            capture_output=True,
            text=True,
            cwd=str(target_dir)
        )
        
        if result.returncode == 0:
            print(f"✅ Python版本: {result.stdout.strip()}")
        else:
            print(f"❌ Python版本测试失败: {result.stderr}")
            return False
        
        # 测试pip
        result = subprocess.run(
            [str(python_exe), "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            cwd=str(target_dir)
        )
        
        if result.returncode == 0:
            print(f"✅ pip版本: {result.stdout.strip()}")
        else:
            print(f"⚠️ pip测试失败: {result.stderr}")
        
        # 测试基本导入
        result = subprocess.run(
            [str(python_exe), "-c", "import sys, os; print(f'Python路径: {sys.executable}'); print(f'工作目录: {os.getcwd()}')"],
            capture_output=True,
            text=True,
            cwd=str(target_dir)
        )
        
        if result.returncode == 0:
            print("✅ 基本导入测试成功")
            print(result.stdout)
        else:
            print(f"⚠️ 基本导入测试失败: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("Python环境设置工具")
    print("=" * 50)
    
    # 设置Python环境
    success = setup_python_environment()
    
    if success:
        # 测试安装
        test_success = test_python_installation()
        
        if test_success:
            print("\n✅ Python环境设置和测试成功！")
            print("现在可以使用独立的Python环境了。")
        else:
            print("\n⚠️ Python环境设置成功，但测试失败")
    else:
        print("\n❌ Python环境设置失败")

if __name__ == "__main__":
    main()
