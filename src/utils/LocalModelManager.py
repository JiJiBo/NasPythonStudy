"""
本地AI模型管理器
支持Qwen2.5-Coder模型的下载、管理和推理
"""

import os
import json
import hashlib
import requests
import threading
from pathlib import Path
from typing import Dict, List, Optional, Callable
from llama_cpp import Llama
import flet as ft

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

class LocalModelManager:
    """本地模型管理器"""
    
    # 预定义的模型列表
    AVAILABLE_MODELS = {
        "qwen2.5-coder-1.5b-q4_k_m": ModelInfo(
            name="qwen2.5-coder-1.5b-q4_k_m",
            size=986 * 1024 * 1024,  # ~986MB
            url="https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf",
            version="2025-01-01",
            description="最轻量模型，CPU快速响应，适合入门用户"
        ),
        "qwen2.5-coder-1.5b-q5_k_m": ModelInfo(
            name="qwen2.5-coder-1.5b-q5_k_m", 
            size=1100 * 1024 * 1024,  # ~1.1GB
            url="https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q5_k_m.gguf",
            version="2025-01-01",
            description="默认推荐模型，平衡性能和精度"
        ),
        "qwen2.5-coder-1.5b-q8_0": ModelInfo(
            name="qwen2.5-coder-1.5b-q8_0",
            size=1650 * 1024 * 1024,  # ~1.65GB
            url="https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q8_0.gguf",
            version="2025-01-01", 
            description="高精度模型，适合高端用户"
        )
    }
    
    def __init__(self):
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        self.current_model = None
        self.llm_instance = None
        self.download_progress = {}
        
    def get_available_models(self) -> Dict[str, ModelInfo]:
        """获取可用模型列表"""
        return self.AVAILABLE_MODELS.copy()
    
    def get_installed_models(self) -> List[ModelInfo]:
        """获取已安装的模型列表"""
        installed = []
        for model_info in self.AVAILABLE_MODELS.values():
            if os.path.exists(model_info.file_path):
                # 检查文件大小是否匹配
                actual_size = os.path.getsize(model_info.file_path)
                if abs(actual_size - model_info.size) < model_info.size * 0.1:  # 允许10%误差
                    installed.append(model_info)
        return installed
    
    def is_model_installed(self, model_name: str) -> bool:
        """检查模型是否已安装"""
        if model_name not in self.AVAILABLE_MODELS:
            return False
        model_info = self.AVAILABLE_MODELS[model_name]
        return os.path.exists(model_info.file_path)
    
    def download_model(self, model_name: str, progress_callback: Optional[Callable] = None, 
                      error_callback: Optional[Callable] = None) -> bool:
        """下载模型"""
        if model_name not in self.AVAILABLE_MODELS:
            if error_callback:
                error_callback(f"未知模型: {model_name}")
            return False
            
        model_info = self.AVAILABLE_MODELS[model_name]
        
        def download_thread():
            try:
                # 创建临时文件
                temp_file = f"{model_info.file_path}.tmp"
                
                # 开始下载
                response = requests.get(model_info.url, stream=True)
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
                                self.download_progress[model_name] = progress
                                progress_callback(model_name, progress, downloaded, total_size)
                
                # 下载完成，重命名文件
                if os.path.exists(model_info.file_path):
                    os.remove(model_info.file_path)
                os.rename(temp_file, model_info.file_path)
                
                # 完成回调
                if progress_callback:
                    progress_callback(model_name, 100, downloaded, total_size)
                    
            except Exception as e:
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                if error_callback:
                    error_callback(f"下载失败: {str(e)}")
        
        # 启动下载线程
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
        return True
    
    def load_model(self, model_name: str) -> bool:
        """加载模型"""
        if model_name not in self.AVAILABLE_MODELS:
            return False
            
        model_info = self.AVAILABLE_MODELS[model_name]
        if not os.path.exists(model_info.file_path):
            return False
            
        try:
            # 释放之前的模型
            if self.llm_instance:
                del self.llm_instance
                self.llm_instance = None
                
            # 加载新模型
            self.llm_instance = Llama(
                model_path=model_info.file_path,
                n_ctx=2048,  # 上下文长度
                n_threads=4,  # 线程数
                verbose=False
            )
            self.current_model = model_name
            return True
            
        except Exception as e:
            print(f"加载模型失败: {str(e)}")
            return False
    
    def get_response(self, prompt: str, max_tokens: int = 512) -> str:
        """获取模型响应"""
        if not self.llm_instance:
            return "错误: 没有加载任何模型"
            
        try:
            # 构建系统提示
            system_prompt = """你是一个专业的Python编程助手，专门帮助用户学习Python编程。
请用简洁、易懂的中文回答用户的问题，并提供实用的代码示例。
如果用户询问代码相关问题，请提供完整的、可运行的代码示例。"""
            
            full_prompt = f"{system_prompt}\n\n用户问题: {prompt}"
            
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
                       max_tokens: int = 512) -> None:
        """流式生成响应"""
        if not self.llm_instance:
            callback("错误: 没有加载任何模型")
            return
            
        try:
            system_prompt = """你是一个专业的Python编程助手，专门帮助用户学习Python编程。
请用简洁、易懂的中文回答用户的问题，并提供实用的代码示例。
如果用户询问代码相关问题，请提供完整的、可运行的代码示例。"""
            
            full_prompt = f"{system_prompt}\n\n用户问题: {prompt}"
            
            # 流式生成
            for chunk in self.llm_instance(
                full_prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=["用户问题:", "\n\n用户问题:"],
                stream=True
            ):
                if 'choices' in chunk and len(chunk['choices']) > 0:
                    delta = chunk['choices'][0].get('text', '')
                    if delta:
                        callback(delta)
                        
        except Exception as e:
            callback(f"生成响应时出错: {str(e)}")
    
    def get_model_status(self) -> Dict:
        """获取模型状态"""
        return {
            "current_model": self.current_model,
            "is_loaded": self.llm_instance is not None,
            "installed_models": [m.name for m in self.get_installed_models()],
            "available_models": list(self.AVAILABLE_MODELS.keys())
        }
    
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
