"""
本地AI模型管理器
支持Qwen2.5-Coder模型的下载、管理和推理
"""

import os
import json
import hashlib
import requests
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable
from collections import defaultdict

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
    print("llama-cpp-python 已安装")
except ImportError as e:
    LLAMA_CPP_AVAILABLE = False
    Llama = None
    print(f"llama-cpp-python 未安装: {e}")

try:
    import flet as ft
except ImportError:
    ft = None

class ModelInfo:
    """模型信息类"""
    def __init__(self, name: str, size: int, url: str, version: str, description: str = ""):
        self.name = name
        self.size = size
        self.url = url
        self.version = version
        self.description = description
        self.file_path = f"models/{name}.gguf"
    
    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "url": self.url,
            "version": self.version,
            "description": self.description,
            "file_path": self.file_path
        }

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
            "last_update": self.last_update
        }

class DownloadEventManager:
    """下载事件管理器"""
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.download_statuses = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅"""
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Dict):
        """发送事件"""
        for callback in self.subscribers[event_type]:
            try:
                callback(data)
            except Exception as e:
                print(f"事件回调错误: {e}")
    
    def get_download_status(self, model_name: str) -> Optional[DownloadStatus]:
        """获取下载状态"""
        return self.download_statuses.get(model_name)
    
    def update_download_status(self, model_name: str, status: DownloadStatus):
        """更新下载状态"""
        self.download_statuses[model_name] = status
        self.emit("download_status_changed", {
            "model_name": model_name,
            "status": status.to_dict()
        })
    
    def get_all_download_statuses(self) -> Dict[str, DownloadStatus]:
        """获取所有下载状态"""
        return self.download_statuses.copy()

class LocalModelManager:
    """本地模型管理器"""
    
    # 预定义的模型列表 - 多个镜像源
    AVAILABLE_MODELS = {
        "qwen2.5-coder-7b-q4_k_m": ModelInfo(
            name="qwen2.5-coder-7b-q4_k_m",
            size=4200 * 1024 * 1024,  # ~4.2GB
            url="https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_k_m.gguf",
            version="2025-01-01",
            description="7B模型轻量版，更好的代码生成能力"
        ),
        "qwen2.5-coder-7b-q5_k_m": ModelInfo(
            name="qwen2.5-coder-7b-q5_k_m", 
            size=5200 * 1024 * 1024,  # ~5.2GB
            url="https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q5_k_m.gguf",
            version="2025-01-01",
            description="7B模型默认版，高质量代码生成，推荐使用"
        ),
        "qwen2.5-coder-7b-q8_0": ModelInfo(
            name="qwen2.5-coder-7b-q8_0",
            size=7800 * 1024 * 1024,  # ~7.8GB
            url="https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q8_0.gguf",
            version="2025-01-01", 
            description="7B模型高精度版，最佳代码生成能力"
        )
    }
    
    # 镜像源列表 - 支持7B模型
    MIRROR_SOURCES = {
        "huggingface": "https://huggingface.co/Qwen/",
        "hf-mirror": "https://hf-mirror.com/Qwen/",
        "modelscope-direct": "https://modelscope.oss-cn-beijing.aliyuncs.com/models/qwen/",
        "modelscope": "https://www.modelscope.cn/api/v1/models/qwen/",
        "huggingface-mirror": "https://huggingface.co.uk/Qwen/",
        "hf-mirror-cn": "https://hf-mirror.com/Qwen/",
        "modelscope-cdn": "https://cdn.modelscope.cn/models/qwen/"
    }
    
    def __init__(self):
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        self.current_model = None
        self.llm_instance = None
        self.download_progress = {}
        self.working_mirrors = {}  # 缓存可用的镜像源
        self.download_sessions = {}  # 存储下载会话信息
        self.event_manager = DownloadEventManager()  # 事件管理器
        self._load_download_statuses()  # 加载未完成的下载状态
        
    def get_available_models(self) -> Dict[str, ModelInfo]:
        """获取可用模型列表"""
        print(f"可用模型数量: {len(self.AVAILABLE_MODELS)}")
        for name, model_info in self.AVAILABLE_MODELS.items():
            print(f"  - {name}: {model_info.file_path}")
        return self.AVAILABLE_MODELS.copy()
    
    def _load_download_statuses(self):
        """加载未完成的下载状态"""
        incomplete = self.get_incomplete_downloads()
        for model_name, download_info in incomplete.items():
            status = DownloadStatus(
                model_name=model_name,
                total_size=download_info["total_size"],
                downloaded_size=download_info["downloaded_size"]
            )
            status.status = "paused"  # 未完成的下载标记为暂停状态
            status.update_progress(download_info["downloaded_size"], download_info["total_size"])
            self.event_manager.update_download_status(model_name, status)
    
    def subscribe_download_events(self, callback: Callable):
        """订阅下载事件"""
        self.event_manager.subscribe("download_status_changed", callback)
    
    def unsubscribe_download_events(self, callback: Callable):
        """取消订阅下载事件"""
        self.event_manager.unsubscribe("download_status_changed", callback)
    
    def get_incomplete_downloads(self) -> Dict[str, Dict]:
        """获取未完成的下载列表"""
        incomplete = {}
        
        for model_name, model_info in self.AVAILABLE_MODELS.items():
            temp_file = f"{model_info.file_path}.tmp"
            if os.path.exists(temp_file):
                try:
                    downloaded_size = os.path.getsize(temp_file)
                    total_size = model_info.size
                    progress = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                    
                    incomplete[model_name] = {
                        "downloaded_size": downloaded_size,
                        "total_size": total_size,
                        "progress": progress,
                        "temp_file": temp_file,
                        "model_info": model_info
                    }
                except Exception as e:
                    print(f"检查未完成下载时出错 {model_name}: {e}")
        
        return incomplete
    
    def resume_download(self, model_name: str, progress_callback: Optional[Callable] = None, 
                       error_callback: Optional[Callable] = None, success_callback: Optional[Callable] = None) -> bool:
        """恢复下载"""
        incomplete = self.get_incomplete_downloads()
        
        if model_name not in incomplete:
            if error_callback:
                error_callback("没有找到未完成的下载")
            return False
        
        download_info = incomplete[model_name]
        model_info = download_info["model_info"]
        
        print(f"恢复下载 {model_name}，已下载 {download_info['downloaded_size']//1024//1024}MB")
        
        # 获取最佳镜像源URL
        download_url = self.get_best_mirror_url(model_name)
        
        def download_thread():
            temp_file = download_info["temp_file"]
            max_retries = 3
            retry_delay = 5
            
            for attempt in range(max_retries):
                try:
                    # 从断点续传
                    downloaded = download_info["downloaded_size"]
                    resume_header = {'Range': f'bytes={downloaded}-'}
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    headers.update(resume_header)
                    
                    response = requests.get(download_url, stream=True, headers=headers, timeout=30)
                    response.raise_for_status()
                    
                    # 获取文件总大小
                    if 'content-range' in response.headers:
                        total_size = int(response.headers['content-range'].split('/')[-1])
                    else:
                        total_size = int(response.headers.get('content-length', 0)) + downloaded
                    
                    # 追加模式继续下载
                    with open(temp_file, 'ab') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                # 更新进度
                                if progress_callback and total_size > 0:
                                    progress = (downloaded / total_size) * 100
                                    self.download_progress[model_name] = progress
                                    progress_callback(model_name, progress, downloaded, total_size)
                    
                    # 下载完成，重命名文件
                    if os.path.exists(model_info.file_path):
                        os.remove(model_info.file_path)
                    os.rename(temp_file, model_info.file_path)
                    
                    # 完成回调
                    if progress_callback:
                        progress_callback(model_name, 100, downloaded, total_size)
                    
                    if success_callback:
                        success_callback()
                    
                    print(f"模型 {model_name} 恢复下载完成")
                    return
                    
                except (requests.exceptions.ConnectionError, 
                        requests.exceptions.Timeout,
                        ConnectionResetError,
                        requests.exceptions.RequestException) as e:
                    
                    print(f"恢复下载尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                    
                    if attempt < max_retries - 1:
                        print(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        if error_callback:
                            error_callback(f"恢复下载失败: 网络连接问题，已重试 {max_retries} 次")
                        
                except Exception as e:
                    print(f"恢复下载出现未知错误: {str(e)}")
                    if error_callback:
                        error_callback(f"恢复下载失败: {str(e)}")
                    break
        
        # 启动下载线程
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
        return True
    
    def test_mirror_availability(self, model_name: str) -> Dict[str, bool]:
        """测试所有镜像源的可用性"""
        if model_name not in self.AVAILABLE_MODELS:
            return {}
        
        model_info = self.AVAILABLE_MODELS[model_name]
        filename = f"qwen2.5-coder-1.5b-instruct-{model_name.split('-')[-1]}.gguf"
        
        results = {}
        
        for mirror_name, base_url in self.MIRROR_SOURCES.items():
            try:
                if mirror_name == "modelscope":
                    # ModelScope API格式
                    test_url = f"{base_url}{filename}"
                elif mirror_name == "modelscope-direct":
                    # ModelScope直接下载格式
                    test_url = f"{base_url}{filename}"
                else:
                    # HuggingFace格式
                    test_url = f"{base_url}{filename}"
                
                print(f"测试镜像源: {mirror_name}")
                print(f"URL: {test_url}")
                
                # 发送GET请求测试（只下载少量数据）
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(test_url, headers=headers, timeout=10, stream=True)
                
                if response.status_code in [200, 206]:  # 200正常，206部分内容（断点续传）
                    results[mirror_name] = True
                    print(f"✅ {mirror_name}: 可用 (状态码: {response.status_code})")
                else:
                    results[mirror_name] = False
                    print(f"❌ {mirror_name}: 不可用 (状态码: {response.status_code})")
                    
            except Exception as e:
                results[mirror_name] = False
                print(f"❌ {mirror_name}: 错误 - {str(e)}")
        
        return results
    
    def get_best_mirror_url(self, model_name: str) -> str:
        """获取最佳镜像源URL"""
        if model_name not in self.AVAILABLE_MODELS:
            return ""
        
        # 如果已经测试过，直接返回缓存结果
        if model_name in self.working_mirrors:
            print(f"使用缓存的镜像源: {model_name}")
            return self.working_mirrors[model_name]
        
        model_info = self.AVAILABLE_MODELS[model_name]
        
        # 现在只有7B模型
        model_series = "Qwen2.5-Coder-7B-Instruct-GGUF"
        filename = f"qwen2.5-coder-7b-instruct-{model_name.split('-')[-1]}.gguf"
        
        # 按优先级测试镜像源（简化版本，避免卡住）
        priority_order = ["hf-mirror", "modelscope-direct", "modelscope-cdn", "huggingface", "modelscope", "huggingface-mirror", "hf-mirror-cn"]
        
        # 直接使用第一个可用的镜像源，不进行网络测试
        for mirror_name in priority_order:
            if mirror_name not in self.MIRROR_SOURCES:
                continue
                
            base_url = self.MIRROR_SOURCES[mirror_name]
            
            if mirror_name == "modelscope":
                test_url = f"{base_url}{model_series}/repo?Revision=master&FilePath={filename}"
            elif mirror_name == "modelscope-direct":
                test_url = f"{base_url}{model_series}/{filename}"
            elif mirror_name == "modelscope-cdn":
                test_url = f"{base_url}{model_series}/{filename}"
            else:
                test_url = f"{base_url}{model_series}/resolve/main/{filename}"
            
            # 直接使用第一个镜像源，避免网络测试卡住
            self.working_mirrors[model_name] = test_url
            print(f"选择镜像源: {mirror_name} (跳过测试)")
            return test_url
        
        # 如果所有镜像源都失败，返回原始URL
        print("所有镜像源都不可用，使用原始URL")
        return model_info.url
    
    def get_installed_models(self) -> List[ModelInfo]:
        """获取已安装的模型列表"""
        installed = []
        for model_info in self.AVAILABLE_MODELS.values():
            if os.path.exists(model_info.file_path):
                # 只检查文件是否存在，不检查大小
                actual_size = os.path.getsize(model_info.file_path)
                print(f"检查模型 {model_info.name}:")
                print(f"  文件路径: {model_info.file_path}")
                print(f"  实际大小: {actual_size:,} 字节 ({actual_size//1024//1024}MB)")
                print(f"  ✅ 模型已安装")
                installed.append(model_info)
        print(f"已安装的模型数量: {len(installed)}")
        for model in installed:
            print(f"  - {model.name}")
        return installed
    
    def is_model_installed(self, model_name: str) -> bool:
        """检查模型是否已安装"""
        if model_name not in self.AVAILABLE_MODELS:
            print(f"模型 {model_name} 不在可用模型列表中")
            return False
        model_info = self.AVAILABLE_MODELS[model_name]
        exists = os.path.exists(model_info.file_path)
        print(f"检查模型文件: {model_info.file_path}, 存在: {exists}")
        
        if exists:
            # 只检查文件是否存在，不检查大小
            actual_size = os.path.getsize(model_info.file_path)
            print(f"✅ 模型 {model_name} 已安装 (大小: {actual_size//1024//1024}MB)")
            return True
        else:
            print(f"❌ 模型 {model_name} 文件不存在")
            return False
    
    def download_model(self, model_name: str, progress_callback: Optional[Callable] = None, 
                      error_callback: Optional[Callable] = None, success_callback: Optional[Callable] = None) -> bool:
        """下载模型"""
        if model_name not in self.AVAILABLE_MODELS:
            if error_callback:
                error_callback(f"未知模型: {model_name}")
            return False
            
        model_info = self.AVAILABLE_MODELS[model_name]
        
        # 创建下载状态
        download_status = DownloadStatus(model_name, model_info.size)
        download_status.status = "downloading"
        download_status.start_time = time.time()
        self.event_manager.update_download_status(model_name, download_status)
        
        # 获取最佳镜像源URL
        download_url = self.get_best_mirror_url(model_name)
        print(f"使用下载URL: {download_url}")
        
        def download_thread():
            temp_file = f"{model_info.file_path}.tmp"
            max_retries = 3
            retry_delay = 5  # 重试延迟（秒）
            
            for attempt in range(max_retries):
                try:
                    # 如果文件已存在且不是第一次尝试，从断点续传
                    resume_header = {}
                    if attempt > 0 and os.path.exists(temp_file):
                        downloaded = os.path.getsize(temp_file)
                        resume_header['Range'] = f'bytes={downloaded}-'
                        print(f"断点续传，从 {downloaded} 字节开始")
                    else:
                        downloaded = 0
                    
                    # 开始下载
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    headers.update(resume_header)
                    
                    response = requests.get(download_url, stream=True, headers=headers, timeout=30)
                    response.raise_for_status()
                    
                    # 获取文件总大小
                    if 'content-range' in response.headers:
                        # 断点续传的情况
                        total_size = int(response.headers['content-range'].split('/')[-1])
                    else:
                        total_size = int(response.headers.get('content-length', 0))
                    
                    # 打开文件（追加模式用于断点续传）
                    mode = 'ab' if downloaded > 0 else 'wb'
                    with open(temp_file, mode) as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                # 更新进度
                                if progress_callback and total_size > 0:
                                    progress = (downloaded / total_size) * 100
                                    self.download_progress[model_name] = progress
                                    progress_callback(model_name, progress, downloaded, total_size)
                    
                    # 下载完成，重命名文件
                    if os.path.exists(model_info.file_path):
                        os.remove(model_info.file_path)
                    os.rename(temp_file, model_info.file_path)
                    
                    # 完成回调
                    if progress_callback:
                        progress_callback(model_name, 100, downloaded, total_size)
                    
                    # 成功回调
                    if success_callback:
                        success_callback()
                    
                    print(f"模型 {model_name} 下载完成")
                    return  # 成功下载，退出重试循环
                    
                except (requests.exceptions.ConnectionError, 
                        requests.exceptions.Timeout,
                        ConnectionResetError,
                        requests.exceptions.RequestException) as e:
                    
                    print(f"下载尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                    
                    if attempt < max_retries - 1:
                        print(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避
                    else:
                        # 最后一次尝试失败
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                        if error_callback:
                            error_callback(f"下载失败: 网络连接问题，已重试 {max_retries} 次")
                        
                except Exception as e:
                    # 其他类型的错误，不重试
                    print(f"下载出现未知错误: {str(e)}")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    if error_callback:
                        error_callback(f"下载失败: {str(e)}")
                    break
        
        # 启动下载线程
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
        return True
    
    def load_model(self, model_name: str) -> bool:
        """加载模型"""
        print(f"开始加载模型: {model_name}")
        
        if not LLAMA_CPP_AVAILABLE:
            print("llama-cpp-python 未安装，无法加载模型")
            return False
            
        if model_name not in self.AVAILABLE_MODELS:
            print(f"模型 {model_name} 不在可用模型列表中")
            return False
            
        model_info = self.AVAILABLE_MODELS[model_name]
        print(f"模型文件路径: {model_info.file_path}")
        
        if not os.path.exists(model_info.file_path):
            print(f"模型文件不存在: {model_info.file_path}")
            return False
            
        print(f"模型文件存在，开始加载...")
        
        try:
            # 释放之前的模型
            if self.llm_instance:
                print("释放之前的模型实例")
                del self.llm_instance
                self.llm_instance = None
                
            # 加载新模型
            print(f"正在加载模型: {model_info.file_path}")
            self.llm_instance = Llama(
                model_path=model_info.file_path,
                n_ctx=2048,  # 上下文长度
                n_threads=4,  # 线程数
                verbose=False
            )
            self.current_model = model_name
            print(f"模型加载成功: {model_name}")
            return True
            
        except Exception as e:
            print(f"加载模型失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _clean_prompt(self, prompt: str) -> str:
        """清理prompt，移除错误信息和重复内容，限制长度"""
        if "生成响应时出错" in prompt or "错误:" in prompt:
            # 提取最后一个用户问题
            lines = prompt.split('\n')
            user_questions = []
            for line in lines:
                if line.startswith('用户: '):
                    user_questions.append(line[3:].strip())
            
            if user_questions:
                return user_questions[-1]  # 使用最后一个用户问题
            else:
                return "你好"  # 默认问题
        
        # 移除重复的对话模式
        lines = prompt.split('\n')
        cleaned_lines = []
        seen_patterns = set()
        
        for line in lines:
            # 跳过重复的"用户: 你好"模式
            if line.strip() in seen_patterns and line.startswith('用户: '):
                continue
            seen_patterns.add(line.strip())
            cleaned_lines.append(line)
        
        result = '\n'.join(cleaned_lines)
        
        # 限制总长度，避免超出上下文窗口
        if len(result) > 1000:
            result = result[:1000] + "..."
        
        return result
    
    def is_model_loaded(self) -> bool:
        """检查是否有模型已加载"""
        return self.llm_instance is not None and self.current_model is not None
    
    def get_loaded_model_name(self) -> Optional[str]:
        """获取当前加载的模型名称"""
        return self.current_model if self.is_model_loaded() else None
    
    def get_model_status(self) -> dict:
        """获取模型状态信息"""
        return {
            "is_loaded": self.is_model_loaded(),
            "current_model": self.current_model,
            "available_models": list(self.AVAILABLE_MODELS.keys()),
            "installed_models": [name for name in self.AVAILABLE_MODELS.keys() 
                               if self.is_model_installed(name)]
        }
    
    def get_response(self, prompt: str, max_tokens: int = 512) -> str:
        """获取模型响应"""
        if not LLAMA_CPP_AVAILABLE:
            return "错误: llama-cpp-python 未安装"
            
        if not self.llm_instance:
            return "错误: 没有加载任何模型"
            
        try:
            # 构建系统提示
            system_prompt = """你是一个专业的Python编程助手，专门帮助用户学习Python编程。
请用简洁、易懂的中文回答用户的问题，并提供实用的代码示例。
如果用户询问代码相关问题，请提供完整的、可运行的代码示例。"""
            
            # 清理prompt，移除错误信息
            clean_prompt = self._clean_prompt(prompt)
            full_prompt = f"{system_prompt}\n\n用户问题: {clean_prompt}"
            
            response = self.llm_instance(
                full_prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=["用户问题:", "\n\n用户问题:"]
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            return f"生成响应时出错: {str(e)}"
    
    def stream_response(self, prompt: str, callback: Callable[[str], None], 
                       error_callback: Callable[[str], None] = None, max_tokens: int = 512) -> None:
        """流式生成响应"""
        print(f"stream_response 被调用，prompt: {prompt[:100]}...")
        
        if not LLAMA_CPP_AVAILABLE:
            error_msg = "错误: llama-cpp-python 未安装"
            print(error_msg)
            if error_callback:
                error_callback(error_msg)
            else:
                callback(error_msg)
            return
            
        if not self.llm_instance:
            error_msg = "错误: 没有加载任何模型"
            print(error_msg)
            if error_callback:
                error_callback(error_msg)
            else:
                callback(error_msg)
            return
            
        try:
            # 简化系统提示，减少token使用
            system_prompt = "你是Python编程助手，用中文回答并提供代码示例。"
            
            # 清理prompt，移除错误信息并限制长度
            clean_prompt = self._clean_prompt(prompt)
            
            # 限制prompt长度，避免超出上下文窗口
            if len(clean_prompt) > 1000:
                clean_prompt = clean_prompt[:1000] + "..."
            
            full_prompt = f"{system_prompt}\n\n问题: {clean_prompt}\n\n回答:"
            print(f"清理后的prompt: {clean_prompt}")
            print(f"完整prompt: {full_prompt[:200]}...")
            
            # 流式生成
            print("开始流式生成...")
            try:
                # 使用正确的 llama-cpp-python API
                response = self.llm_instance(
                    full_prompt,
                    max_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    stop=["用户:", "用户问题:", "\n\n用户:", "\n\n用户问题:", "助手:", "\n\n助手:"],
                    stream=True
                )
                
                for chunk in response:
                    print(f"收到chunk: {chunk}")
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        delta = chunk['choices'][0].get('text', '')
                        if delta:
                            print(f"发送delta: {delta}")
                            callback(delta)
                            
            except Exception as stream_error:
                print(f"流式生成错误: {stream_error}")
                # 如果流式生成失败，尝试非流式生成
                print("尝试非流式生成...")
                try:
                    response = self.llm_instance(
                        full_prompt,
                        max_tokens=max_tokens,
                        temperature=0.7,
                        top_p=0.9,
                        stop=["用户:", "用户问题:", "\n\n用户:", "\n\n用户问题:", "助手:", "\n\n助手:"],
                        stream=False
                    )
                    if 'choices' in response and len(response['choices']) > 0:
                        text = response['choices'][0].get('text', '')
                        if text:
                            print(f"非流式响应: {text}")
                            callback(text)
                except Exception as non_stream_error:
                    print(f"非流式生成也失败: {non_stream_error}")
                    raise non_stream_error
                        
        except Exception as e:
            error_msg = f"生成响应时出错: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            if error_callback:
                error_callback(error_msg)
            else:
                callback(error_msg)
    
    def get_model_status(self) -> Dict:
        """获取模型状态"""
        return {
            "current_model": self.current_model,
            "is_loaded": self.llm_instance is not None,
            "installed_models": [m.name for m in self.get_installed_models()],
            "available_models": list(self.AVAILABLE_MODELS.keys()),
            "llama_cpp_available": LLAMA_CPP_AVAILABLE
        }
    
    def test_model_loading(self, model_name: str) -> Dict:
        """测试模型加载"""
        result = {
            "model_name": model_name,
            "llama_cpp_available": LLAMA_CPP_AVAILABLE,
            "model_in_list": model_name in self.AVAILABLE_MODELS,
            "file_exists": False,
            "file_path": "",
            "load_success": False,
            "error_message": ""
        }
        
        if not LLAMA_CPP_AVAILABLE:
            result["error_message"] = "llama-cpp-python 未安装"
            return result
            
        if model_name not in self.AVAILABLE_MODELS:
            result["error_message"] = "模型不在可用列表中"
            return result
            
        model_info = self.AVAILABLE_MODELS[model_name]
        result["file_path"] = model_info.file_path
        result["file_exists"] = os.path.exists(model_info.file_path)
        
        if not result["file_exists"]:
            result["error_message"] = "模型文件不存在"
            return result
            
        try:
            # 尝试加载模型
            test_llm = Llama(
                model_path=model_info.file_path,
                n_ctx=512,  # 使用较小的上下文长度进行测试
                n_threads=2,  # 使用较少的线程
                verbose=False
            )
            result["load_success"] = True
            del test_llm  # 释放测试实例
        except Exception as e:
            result["error_message"] = str(e)
            
        return result
    
    def delete_model(self, model_name: str) -> bool:
        """删除模型"""
        if model_name not in self.AVAILABLE_MODELS:
            return False
            
        model_info = self.AVAILABLE_MODELS[model_name]
        if os.path.exists(model_info.file_path):
            try:
                os.remove(model_info.file_path)
                # 如果删除的是当前加载的模型，释放实例
                if self.current_model == model_name:
                    if self.llm_instance:
                        del self.llm_instance
                        self.llm_instance = None
                    self.current_model = None
                return True
            except Exception as e:
                print(f"删除模型失败: {str(e)}")
                return False
        return False

# 全局模型管理器实例
local_model_manager = LocalModelManager()
