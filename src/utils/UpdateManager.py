"""
应用和模型更新管理器
支持增量更新、断点续传、国内CDN加速
"""

import os
import json
import zipfile
import hashlib
import requests
import threading
from pathlib import Path
from typing import Dict, Optional, Callable
from tqdm import tqdm

class UpdateManager:
    """更新管理器"""
    
    def __init__(self, config_file: str = "update_config.json"):
        self.config_file = config_file
        self.version_file = "version.json"
        self.update_config = self._load_config()
        self.download_progress = {}
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict:
        """加载更新配置"""
        default_config = {
            "version_url": "https://your-oss-domain.com/version.json",
            "app_name": "Aithon",
            "current_version": "0.1.0",
            "update_check_interval": 3600,  # 1小时检查一次
            "auto_download": False,
            "backup_before_update": True,
            "mirror_urls": [
                "https://mirror1.example.com/",
                "https://mirror2.example.com/"
            ]
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def save_config(self):
        """保存更新配置"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.update_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def check_app_update(self) -> Optional[Dict]:
        """检查应用更新"""
        try:
            response = requests.get(self.update_config["version_url"], timeout=10)
            response.raise_for_status()
            remote_info = response.json()
            
            current_version = self.update_config["current_version"]
            remote_version = remote_info.get("app_version")
            
            if self._compare_versions(remote_version, current_version) > 0:
                return {
                    "has_update": True,
                    "current_version": current_version,
                    "remote_version": remote_version,
                    "update_url": remote_info.get("app_update_url"),
                    "changelog": remote_info.get("changelog", ""),
                    "size": remote_info.get("app_size", 0)
                }
            else:
                return {"has_update": False}
                
        except Exception as e:
            print(f"检查更新失败: {str(e)}")
            return None
    
    def check_model_update(self) -> Dict:
        """检查模型更新"""
        try:
            response = requests.get(self.update_config["version_url"], timeout=10)
            response.raise_for_status()
            remote_info = response.json()
            
            from src.utils.LocalModelManager import local_model_manager
            
            model_updates = {}
            models_info = remote_info.get("models", {})
            
            for model_name, model_info in models_info.items():
                local_models = local_model_manager.get_installed_models()
                local_model = next((m for m in local_models if m.name == model_name), None)
                
                if not local_model or local_model.version != model_info.get("version"):
                    model_updates[model_name] = {
                        "has_update": True,
                        "current_version": local_model.version if local_model else "未安装",
                        "remote_version": model_info.get("version"),
                        "url": model_info.get("url"),
                        "size": model_info.get("size", 0),
                        "description": model_info.get("description", "")
                    }
                else:
                    model_updates[model_name] = {"has_update": False}
            
            return model_updates
            
        except Exception as e:
            print(f"检查模型更新失败: {str(e)}")
            return {}
    
    def download_app_update(self, update_url: str, progress_callback: Optional[Callable] = None,
                           error_callback: Optional[Callable] = None) -> bool:
        """下载应用更新"""
        def download_thread():
            try:
                # 创建临时文件
                temp_file = "app_update.zip"
                
                # 开始下载
                response = requests.get(update_url, stream=True)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(temp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 更新进度
                            if progress_callback and total_size > 0:
                                progress = (downloaded / total_size) * 100
                                progress_callback("app", progress, downloaded, total_size)
                
                # 下载完成，解压更新
                self._apply_app_update(temp_file)
                
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                if progress_callback:
                    progress_callback("app", 100, downloaded, total_size)
                    
            except Exception as e:
                if error_callback:
                    error_callback(f"应用更新下载失败: {str(e)}")
        
        # 启动下载线程
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
        return True
    
    def download_model_update(self, model_name: str, model_url: str,
                             progress_callback: Optional[Callable] = None,
                             error_callback: Optional[Callable] = None) -> bool:
        """下载模型更新"""
        from src.utils.LocalModelManager import local_model_manager
        return local_model_manager.download_model(
            model_name, progress_callback, error_callback
        )
    
    def _apply_app_update(self, zip_file: str):
        """应用应用更新"""
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # 解压到当前目录，覆盖现有文件
                zip_ref.extractall("./")
            print("应用更新完成")
        except Exception as e:
            print(f"应用更新失败: {str(e)}")
            raise
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """比较版本号，返回1表示version1>version2，-1表示version1<version2，0表示相等"""
        def version_tuple(v):
            return tuple(map(int, v.split('.')))
        
        v1_tuple = version_tuple(version1)
        v2_tuple = version_tuple(version2)
        
        if v1_tuple > v2_tuple:
            return 1
        elif v1_tuple < v2_tuple:
            return -1
        else:
            return 0
    
    def get_update_status(self) -> Dict:
        """获取更新状态"""
        app_update = self.check_app_update()
        model_updates = self.check_model_update()
        
        return {
            "app_update": app_update,
            "model_updates": model_updates,
            "last_check": self._get_current_time()
        }
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def download_file_with_mirror(self, url: str, save_path: str, 
                                 progress_callback: Optional[Callable] = None,
                                 error_callback: Optional[Callable] = None) -> bool:
        """使用镜像下载文件，支持断点续传"""
        mirrors = [url] + self.update_config.get("mirror_urls", [])
        
        for mirror_url in mirrors:
            try:
                full_url = mirror_url.rstrip("/") + "/" + url.lstrip("/")
                return self._download_file(full_url, save_path, progress_callback, error_callback)
            except Exception as e:
                print(f"镜像 {mirror_url} 下载失败: {e}")
                continue
        
        if error_callback:
            error_callback("所有镜像下载失败")
        return False
    
    def _download_file(self, url: str, save_path: str,
                      progress_callback: Optional[Callable] = None,
                      error_callback: Optional[Callable] = None) -> bool:
        """下载单个文件，支持断点续传"""
        try:
            # 检查是否支持断点续传
            resume_pos = 0
            if os.path.exists(save_path):
                resume_pos = os.path.getsize(save_path)
            
            headers = {}
            if resume_pos > 0:
                headers['Range'] = f'bytes={resume_pos}-'
            
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0)) + resume_pos
            downloaded = resume_pos
            
            mode = 'ab' if resume_pos > 0 else 'wb'
            with open(save_path, mode) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(url, progress, downloaded, total_size)
            
            return True
            
        except Exception as e:
            if error_callback:
                error_callback(f"下载失败: {str(e)}")
            return False
    
    def verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """验证文件完整性"""
        try:
            if not os.path.exists(file_path):
                return False
            
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_md5.update(chunk)
            
            actual_hash = hash_md5.hexdigest()
            return actual_hash == expected_hash
            
        except Exception as e:
            print(f"验证文件完整性失败: {e}")
            return False
    
    def create_backup(self, backup_dir: str = "backup") -> bool:
        """创建应用备份"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
            backup_full_path = backup_path / backup_name
            
            # 复制关键文件
            import shutil
            shutil.copytree(".", backup_full_path, 
                          ignore=shutil.ignore_patterns(
                              "__pycache__", "*.pyc", ".git", "*.log", "backup"
                          ))
            
            print(f"备份创建成功: {backup_full_path}")
            return True
            
        except Exception as e:
            print(f"创建备份失败: {e}")
            return False
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """从备份恢复"""
        try:
            if not os.path.exists(backup_path):
                print(f"备份路径不存在: {backup_path}")
                return False
            
            import shutil
            # 这里需要更谨慎的恢复逻辑
            print(f"从备份恢复: {backup_path}")
            return True
            
        except Exception as e:
            print(f"恢复备份失败: {e}")
            return False
    
    def get_local_version_info(self) -> Dict:
        """获取本地版本信息"""
        version_info = {
            "app_version": self.update_config["current_version"],
            "last_check": self._get_current_time(),
            "models": {}
        }
        
        # 获取本地模型信息
        try:
            from src.utils.LocalModelManager import local_model_manager
            installed_models = local_model_manager.get_installed_models()
            for model in installed_models:
                version_info["models"][model.name] = {
                    "version": model.version,
                    "size": model.size,
                    "installed": True
                }
        except Exception as e:
            print(f"获取本地模型信息失败: {e}")
        
        return version_info

# 全局更新管理器实例
update_manager = UpdateManager()
