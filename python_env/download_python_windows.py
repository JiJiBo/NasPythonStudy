#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows专用Python下载脚本
下载Python 3.11.9嵌入版并解压到python_env文件夹
"""

import os
import sys
import requests
import zipfile
import shutil
from pathlib import Path

def download_python_windows():
    """下载Windows版本的Python"""
    print("=== 下载Windows版本Python ===")
    
    # 目标目录
    target_dir = Path("python_env")
    target_dir.mkdir(exist_ok=True)
    
    # Python 3.11.9 嵌入版下载信息
    python_version = "3.11.9"
    download_url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-amd64.zip"
    zip_filename = f"python-{python_version}-embed-amd64.zip"
    zip_path = target_dir / zip_filename
    extract_dir = target_dir / f"python-{python_version}-embed-amd64"
    
    print(f"下载URL: {download_url}")
    print(f"保存路径: {zip_path}")
    print(f"解压目录: {extract_dir}")
    
    # 1. 下载文件
    print("\n1. 正在下载Python...")
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r下载进度: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✅ 下载完成: {zip_path}")
        
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        return False
    
    # 2. 解压文件
    print("\n2. 正在解压Python...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        
        print(f"✅ 解压完成: {extract_dir}")
        
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False
    
    # 3. 设置Python环境
    print("\n3. 正在设置Python环境...")
    try:
        # 重命名目录为python
        python_dir = target_dir / "python"
        if python_dir.exists():
            shutil.rmtree(python_dir)
        extract_dir.rename(python_dir)
        
        # 创建python.exe的副本（如果不存在）
        python_exe = python_dir / "python.exe"
        if not python_exe.exists():
            # 查找python可执行文件
            for exe_name in ["python.exe", "python"]:
                exe_path = python_dir / exe_name
                if exe_path.exists():
                    shutil.copy2(exe_path, python_exe)
                    break
        
        print(f"✅ Python环境设置完成: {python_dir}")
        
    except Exception as e:
        print(f"❌ 设置Python环境失败: {e}")
        return False
    
    # 4. 安装pip
    print("\n4. 正在安装pip...")
    try:
        # 下载get-pip.py
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = python_dir / "get-pip.py"
        
        response = requests.get(get_pip_url)
        response.raise_for_status()
        
        with open(get_pip_path, 'wb') as f:
            f.write(response.content)
        
        # 安装pip
        import subprocess
        result = subprocess.run(
            [str(python_exe), str(get_pip_path)],
            capture_output=True,
            text=True,
            cwd=str(python_dir)
        )
        
        if result.returncode == 0:
            print("✅ pip安装成功")
        else:
            print(f"⚠️ pip安装可能有问题: {result.stderr}")
        
    except Exception as e:
        print(f"❌ pip安装失败: {e}")
    
    # 5. 创建启动脚本
    print("\n5. 正在创建启动脚本...")
    try:
        launcher_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python启动器 - 版本 {python_version}
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
    print(f"Python {python_version} 启动器")
    print(f"Python目录: {{python_dir}}")
    print(f"Python版本: {{sys.version}}")
    
    # 测试导入
    try:
        import sys
        print(f"Python可执行文件: {{sys.executable}}")
    except Exception as e:
        print(f"导入测试失败: {{e}}")
'''
        
        launcher_path = python_dir / "launcher.py"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print("✅ 启动脚本创建完成")
        
    except Exception as e:
        print(f"❌ 创建启动脚本失败: {e}")
    
    # 6. 清理下载文件
    print("\n6. 正在清理下载文件...")
    try:
        zip_path.unlink()
        print("✅ 清理完成")
    except:
        print("⚠️ 清理失败")
    
    print("\n" + "=" * 50)
    print("🎉 Python安装完成！")
    print(f"Python路径: {python_exe}")
    print(f"版本: {python_version}")
    print(f"目录: {python_dir}")
    
    return True

def test_python_installation():
    """测试Python安装"""
    print("\n=== 测试Python安装 ===")
    
    python_dir = Path("python_env/python")
    python_exe = python_dir / "python.exe"
    
    if not python_exe.exists():
        print("❌ Python可执行文件不存在")
        return False
    
    try:
        import subprocess
        
        # 测试Python版本
        result = subprocess.run(
            [str(python_exe), "--version"],
            capture_output=True,
            text=True,
            cwd=str(python_dir)
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
            cwd=str(python_dir)
        )
        
        if result.returncode == 0:
            print(f"✅ pip版本: {result.stdout.strip()}")
        else:
            print(f"⚠️ pip测试失败: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("Windows专用Python下载工具")
    print("=" * 50)
    
    # 检查操作系统
    if sys.platform != "win32":
        print("❌ 此脚本仅支持Windows系统")
        return
    
    # 下载并安装Python
    success = download_python_windows()
    
    if success:
        # 测试安装
        test_success = test_python_installation()
        
        if test_success:
            print("\n✅ Python安装和测试成功！")
            print("现在可以使用独立的Python环境了。")
        else:
            print("\n⚠️ Python安装成功，但测试失败")
    else:
        print("\n❌ Python安装失败")

if __name__ == "__main__":
    main()
