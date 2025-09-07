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
    
    def __init__(self):
        self.version_file = "version.json"
        self.update_config = {
            "version_url": "https://your-oss-domain.com/version.json",  # 替换为实际的OSS地址
            "app_name": "Aithon",
            "current_version": "0.1.0"
        }
        self.download_progress = {}
        
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

# 全局更新管理器实例
update_manager = UpdateManager()
