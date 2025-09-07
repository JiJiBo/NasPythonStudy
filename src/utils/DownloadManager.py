"""
基于事件系统的下载管理器
支持订阅监听方式更新进度，退出后重新进入可恢复下载
"""

import os
import time
import threading
import requests
from pathlib import Path
from typing import Dict, List, Optional, Callable
from collections import defaultdict

class DownloadStatus:
    """下载状态类"""
    def __init__(self, model_name: str, total_size: int = 0, downloaded_size: int = 0):
        self.model_name = model_name
        self.total_size = total_size
        self.downloaded_size = downloaded_size
        self.progress = 0.0
        self.status = "idle"  # idle, downloading, paused, completed, error
        self.error_message = ""
        self.temp_file = f"models/{model_name}.gguf.tmp"
        self.start_time = None
        self.last_update = None
        self.download_url = ""
    
    def update_progress(self, downloaded: int, total: int):
        self.downloaded_size = downloaded
        self.total_size = total
        self.progress = (downloaded / total * 100) if total > 0 else 0
        self.last_update = time.time()
    
    def to_dict(self):
        return {
            "model_name": self.model_name,
            "total_size": self.total_size,
            "downloaded_size": self.downloaded_size,
            "progress": self.progress,
            "status": self.status,
            "error_message": self.error_message,
            "temp_file": self.temp_file,
            "start_time": self.start_time,
            "last_update": self.last_update,
            "download_url": self.download_url
        }

class DownloadEventManager:
    """下载事件管理器"""
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.download_statuses = {}
        self.lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        with self.lock:
            self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅"""
        with self.lock:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Dict):
        """发送事件"""
        with self.lock:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"事件回调错误: {e}")
    
    def get_download_status(self, model_name: str) -> Optional[DownloadStatus]:
        """获取下载状态"""
        with self.lock:
            return self.download_statuses.get(model_name)
    
    def update_download_status(self, model_name: str, status: DownloadStatus):
        """更新下载状态"""
        with self.lock:
            self.download_statuses[model_name] = status
            self.emit("download_status_changed", {
                "model_name": model_name,
                "status": status.to_dict()
            })
    
    def get_all_download_statuses(self) -> Dict[str, DownloadStatus]:
        """获取所有下载状态"""
        with self.lock:
            return self.download_statuses.copy()

class DownloadManager:
    """下载管理器"""
    
    def __init__(self):
        self.event_manager = DownloadEventManager()
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        self._load_incomplete_downloads()
    
    def _load_incomplete_downloads(self):
        """加载未完成的下载"""
        for temp_file in self.models_dir.glob("*.tmp"):
            model_name = temp_file.stem.replace(".gguf", "")
            if os.path.exists(temp_file):
                try:
                    downloaded_size = os.path.getsize(temp_file)
                    # 这里需要从模型信息获取总大小，暂时使用估算值
                    total_size = 1000 * 1024 * 1024  # 1GB估算
                    progress = (downloaded_size / total_size * 100) if total_size > 0 else 0
                    
                    status = DownloadStatus(model_name, total_size, downloaded_size)
                    status.status = "paused"
                    status.update_progress(downloaded_size, total_size)
                    
                    self.event_manager.update_download_status(model_name, status)
                    print(f"发现未完成的下载: {model_name} ({progress:.1f}%)")
                except Exception as e:
                    print(f"加载未完成下载时出错 {model_name}: {e}")
    
    def subscribe_download_events(self, callback: Callable):
        """订阅下载事件"""
        self.event_manager.subscribe("download_status_changed", callback)
    
    def unsubscribe_download_events(self, callback: Callable):
        """取消订阅下载事件"""
        self.event_manager.unsubscribe("download_status_changed", callback)
    
    def get_download_status(self, model_name: str) -> Optional[DownloadStatus]:
        """获取下载状态"""
        return self.event_manager.get_download_status(model_name)
    
    def get_all_download_statuses(self) -> Dict[str, DownloadStatus]:
        """获取所有下载状态"""
        return self.event_manager.get_all_download_statuses()
    
    def start_download(self, model_name: str, download_url: str, total_size: int = 0) -> bool:
        """开始下载"""
        # 检查是否已有下载状态
        existing_status = self.get_download_status(model_name)
        if existing_status and existing_status.status == "downloading":
            print(f"模型 {model_name} 正在下载中")
            return False
        
        # 创建下载状态
        status = DownloadStatus(model_name, total_size)
        status.status = "downloading"
        status.start_time = time.time()
        status.download_url = download_url
        self.event_manager.update_download_status(model_name, status)
        
        # 启动下载线程
        thread = threading.Thread(
            target=self._download_thread,
            args=(model_name, download_url, total_size),
            daemon=True
        )
        thread.start()
        return True
    
    def resume_download(self, model_name: str) -> bool:
        """恢复下载"""
        status = self.get_download_status(model_name)
        if not status or status.status != "paused":
            print(f"没有找到可恢复的下载: {model_name}")
            return False
        
        if not status.download_url:
            print(f"下载URL丢失，无法恢复: {model_name}")
            return False
        
        # 更新状态为下载中
        status.status = "downloading"
        status.start_time = time.time()
        self.event_manager.update_download_status(model_name, status)
        
        # 启动下载线程
        thread = threading.Thread(
            target=self._download_thread,
            args=(model_name, status.download_url, status.total_size),
            daemon=True
        )
        thread.start()
        return True
    
    def pause_download(self, model_name: str) -> bool:
        """暂停下载"""
        status = self.get_download_status(model_name)
        if not status or status.status != "downloading":
            return False
        
        status.status = "paused"
        self.event_manager.update_download_status(model_name, status)
        return True
    
    def cancel_download(self, model_name: str) -> bool:
        """取消下载"""
        status = self.get_download_status(model_name)
        if not status:
            return False
        
        # 删除临时文件
        if os.path.exists(status.temp_file):
            try:
                os.remove(status.temp_file)
            except Exception as e:
                print(f"删除临时文件失败: {e}")
        
        # 更新状态
        status.status = "idle"
        status.downloaded_size = 0
        status.progress = 0
        self.event_manager.update_download_status(model_name, status)
        return True
    
    def _download_thread(self, model_name: str, download_url: str, total_size: int):
        """下载线程"""
        status = self.get_download_status(model_name)
        if not status:
            return
        
        temp_file = status.temp_file
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                # 检查是否被暂停
                if status.status != "downloading":
                    return
                
                # 断点续传
                downloaded = 0
                resume_header = {}
                if os.path.exists(temp_file):
                    downloaded = os.path.getsize(temp_file)
                    resume_header['Range'] = f'bytes={downloaded}-'
                    print(f"断点续传 {model_name}，从 {downloaded} 字节开始")
                
                # 开始下载
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                headers.update(resume_header)
                
                response = requests.get(download_url, stream=True, headers=headers, timeout=30)
                response.raise_for_status()
                
                # 获取文件总大小
                if 'content-range' in response.headers:
                    total_size = int(response.headers['content-range'].split('/')[-1])
                elif 'content-length' in response.headers:
                    total_size = int(response.headers['content-length']) + downloaded
                
                # 更新总大小
                status.total_size = total_size
                
                # 打开文件（追加模式用于断点续传）
                mode = 'ab' if downloaded > 0 else 'wb'
                with open(temp_file, mode) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        # 检查是否被暂停或取消
                        if status.status not in ["downloading"]:
                            return
                        
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 更新进度
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                status.update_progress(downloaded, total_size)
                                self.event_manager.update_download_status(model_name, status)
                
                # 下载完成，重命名文件
                final_file = f"models/{model_name}.gguf"
                if os.path.exists(final_file):
                    os.remove(final_file)
                os.rename(temp_file, final_file)
                
                # 更新完成状态
                status.status = "completed"
                status.update_progress(downloaded, total_size)
                self.event_manager.update_download_status(model_name, status)
                
                print(f"模型 {model_name} 下载完成")
                return
                
            except (requests.exceptions.ConnectionError, 
                    requests.exceptions.Timeout,
                    ConnectionResetError,
                    requests.exceptions.RequestException) as e:
                
                print(f"下载尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                
                if attempt < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    # 最后一次尝试失败
                    status.status = "error"
                    status.error_message = f"网络连接问题，已重试 {max_retries} 次"
                    self.event_manager.update_download_status(model_name, status)
                    
            except Exception as e:
                print(f"下载出现未知错误: {str(e)}")
                status.status = "error"
                status.error_message = str(e)
                self.event_manager.update_download_status(model_name, status)
                break

# 全局下载管理器实例
download_manager = DownloadManager()
