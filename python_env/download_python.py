#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python下载和安装脚本
下载官方Python解释器并解压到python_env文件夹
"""

import os
import sys
import requests
import zipfile
import tarfile
import platform
import shutil
from pathlib import Path
from urllib.parse import urljoin

class PythonDownloader:
    def __init__(self, target_dir="python_env"):
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(exist_ok=True)
        
        # Python官方下载URL
        self.base_url = "https://www.python.org/ftp/python/"
        
        # 推荐的Python版本（稳定且支持CUDA）
        self.recommended_version = "3.11.9"
        
        # 不同平台的下载信息
        self.platform_info = {
            "Windows": {
                "extension": "zip",
                "filename_template": "python-{version}-embed-amd64.zip",
                "extract_dir": "python-{version}-embed-amd64"
            },
            "Linux": {
                "extension": "tgz", 
                "filename_template": "Python-{version}.tgz",
                "extract_dir": "Python-{version}"
            },
            "Darwin": {
                "extension": "tgz",
                "filename_template": "Python-{version}.tgz", 
                "extract_dir": "Python-{version}"
            }
        }
    
    def get_platform_info(self):
        """获取当前平台信息"""
        system = platform.system()
        if system not in self.platform_info:
            raise RuntimeError(f"不支持的操作系统: {system}")
        
        return self.platform_info[system]
    
    def get_download_url(self, version=None):
        """获取下载URL"""
        if version is None:
            version = self.recommended_version
        
        platform_info = self.get_platform_info()
        filename = platform_info["filename_template"].format(version=version)
        
        return urljoin(self.base_url, f"{version}/{filename}")
    
    def get_download_path(self, version=None):
        """获取下载文件路径"""
        if version is None:
            version = self.recommended_version
        
        platform_info = self.get_platform_info()
        filename = platform_info["filename_template"].format(version=version)
        
        return self.target_dir / filename
    
    def download_file(self, url, filepath):
        """下载文件"""
        print(f"正在下载: {url}")
        print(f"保存到: {filepath}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r下载进度: {percent:.1f}%", end='', flush=True)
            
            print(f"\n✅ 下载完成: {filepath}")
            return True
            
        except Exception as e:
            print(f"\n❌ 下载失败: {e}")
            if filepath.exists():
                filepath.unlink()
            return False
    
    def extract_archive(self, archive_path, version=None):
        """解压文件"""
        if version is None:
            version = self.recommended_version
        
        platform_info = self.get_platform_info()
        extract_dir_name = platform_info["extract_dir"].format(version=version)
        extract_path = self.target_dir / extract_dir_name
        
        print(f"正在解压: {archive_path}")
        print(f"解压到: {extract_path}")
        
        try:
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(self.target_dir)
            elif archive_path.suffix in ['.tgz', '.tar.gz']:
                with tarfile.open(archive_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(self.target_dir)
            else:
                raise ValueError(f"不支持的文件格式: {archive_path.suffix}")
            
            print(f"✅ 解压完成: {extract_path}")
            return extract_path
            
        except Exception as e:
            print(f"❌ 解压失败: {e}")
            return None
    
    def setup_python_environment(self, python_dir, version=None):
        """设置Python环境"""
        if version is None:
            version = self.recommended_version
        
        print(f"正在设置Python环境: {python_dir}")
        
        # 创建python.exe的符号链接或复制
        python_exe = python_dir / "python.exe"
        if not python_exe.exists():
            # 查找python可执行文件
            for exe_name in ["python.exe", "python", "python3"]:
                exe_path = python_dir / exe_name
                if exe_path.exists():
                    if platform.system() == "Windows":
                        # Windows下创建副本
                        shutil.copy2(exe_path, python_exe)
                    else:
                        # Linux/macOS下创建符号链接
                        python_exe.symlink_to(exe_path)
                    break
        
        # 创建pip配置
        self.setup_pip(python_dir)
        
        # 创建启动脚本
        self.create_launcher_scripts(python_dir, version)
        
        print(f"✅ Python环境设置完成")
        return python_exe
    
    def setup_pip(self, python_dir):
        """设置pip"""
        print("正在设置pip...")
        
        # 下载get-pip.py
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = python_dir / "get-pip.py"
        
        try:
            response = requests.get(get_pip_url)
            response.raise_for_status()
            
            with open(get_pip_path, 'wb') as f:
                f.write(response.content)
            
            print("✅ get-pip.py下载完成")
            
            # 安装pip
            python_exe = python_dir / "python.exe"
            if python_exe.exists():
                import subprocess
                result = subprocess.run(
                    [str(python_exe), str(get_pip_path)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("✅ pip安装成功")
                else:
                    print(f"⚠️ pip安装可能有问题: {result.stderr}")
            
        except Exception as e:
            print(f"❌ pip设置失败: {e}")
    
    def create_launcher_scripts(self, python_dir, version):
        """创建启动脚本"""
        print("正在创建启动脚本...")
        
        # 创建launcher.py
        launcher_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python启动器 - 版本 {version}
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
    print(f"Python {version} 启动器")
    print(f"Python目录: {{python_dir}}")
    print(f"Python版本: {{sys.version}}")
'''
        
        launcher_path = python_dir / "launcher.py"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print("✅ 启动脚本创建完成")
    
    def download_and_install(self, version=None):
        """下载并安装Python"""
        if version is None:
            version = self.recommended_version
        
        print(f"开始下载并安装Python {version}")
        print("=" * 50)
        
        # 1. 获取下载信息
        download_url = self.get_download_url(version)
        download_path = self.get_download_path(version)
        
        print(f"下载URL: {download_url}")
        print(f"下载路径: {download_path}")
        
        # 2. 下载文件
        if not self.download_file(download_url, download_path):
            return False
        
        # 3. 解压文件
        extract_path = self.extract_archive(download_path, version)
        if not extract_path:
            return False
        
        # 4. 设置Python环境
        python_exe = self.setup_python_environment(extract_path, version)
        if not python_exe:
            return False
        
        # 5. 清理下载文件
        try:
            download_path.unlink()
            print("✅ 清理下载文件完成")
        except:
            print("⚠️ 清理下载文件失败")
        
        print("\n" + "=" * 50)
        print("🎉 Python安装完成！")
        print(f"Python路径: {python_exe}")
        print(f"版本: {version}")
        
        return True

def main():
    """主函数"""
    print("Python下载和安装工具")
    print("=" * 50)
    
    # 检查当前平台
    system = platform.system()
    print(f"当前操作系统: {system}")
    
    if system not in ["Windows", "Linux", "Darwin"]:
        print(f"❌ 不支持的操作系统: {system}")
        return
    
    # 创建下载器
    downloader = PythonDownloader()
    
    # 下载并安装Python
    success = downloader.download_and_install()
    
    if success:
        print("\n✅ Python安装成功！")
        print("现在可以使用独立的Python环境了。")
    else:
        print("\n❌ Python安装失败")

if __name__ == "__main__":
    main()
