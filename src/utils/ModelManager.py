#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地模型管理器
负责下载、管理和加载Hugging Face模型
"""

import os
import json
import shutil
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
import requests
from tqdm import tqdm
from src.utils.DownloadStateManager import download_state_manager

class ModelManager:
    def __init__(self, assets_dir: str = "assets/models"):
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # 国内镜像配置
        self.mirrors = [
            "https://huggingface.co",  # 官方源
            "https://hf-mirror.com",   # 国内镜像1
            "https://huggingface.co",  # 备用官方源
        ]
        self.current_mirror_index = 0
        self.max_retries = 3
        self.retry_delay = 2  # 重试延迟（秒）
        
        # 监听器管理
        self._progress_listeners: Dict[str, List[Callable]] = {}  # {model_name: [listeners]}
        self._status_listeners: List[Callable] = []  # 状态变化监听器
        
        # 支持的模型配置
        self.supported_models = {
            "qwen2.5-0.5b": {
                "repo_id": "Qwen/Qwen2.5-0.5B-Instruct",
                "files": [
                    "config.json",
                    "tokenizer.json",
                    "tokenizer_config.json",
                    "generation_config.json",
                    "model.safetensors",
                    "vocab.json",
                    "merges.txt"
                ],
                "optional_files": [
                    "special_tokens_map.json"
                ],
                "size_mb": 1024,  # 约1GB
                "description": "Qwen2.5-0.5B-Instruct - 轻量级中文对话模型"
            },
            "tinyllama-1.1b": {
                "repo_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                "files": [
                    "config.json",
                    "tokenizer.json",
                    "tokenizer_config.json",
                    "generation_config.json",
                    "model.safetensors",
                    "vocab.json",
                    "merges.txt"
                ],
                "optional_files": [
                    "special_tokens_map.json"
                ],
                "size_mb": 2048,  # 约2GB
                "description": "TinyLlama-1.1B-Chat - 超轻量级英文对话模型"
            }
        }
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """获取模型信息"""
        return self.supported_models.get(model_name)
    
    def get_current_mirror(self) -> str:
        """获取当前镜像地址"""
        return self.mirrors[self.current_mirror_index]
    
    def switch_mirror(self):
        """切换到下一个镜像"""
        self.current_mirror_index = (self.current_mirror_index + 1) % len(self.mirrors)
        print(f"切换到镜像: {self.get_current_mirror()}")
    
    def reset_mirror(self):
        """重置到第一个镜像"""
        self.current_mirror_index = 0
    
    def list_available_models(self) -> Dict[str, Dict[str, Any]]:
        """列出所有可用的模型"""
        return self.supported_models.copy()
    
    def is_model_downloaded(self, model_name: str) -> bool:
        """检查模型是否已下载"""
        model_dir = self.assets_dir / model_name
        if not model_dir.exists():
            return False
        
        model_info = self.get_model_info(model_name)
        if not model_info:
            return False
        
        # 检查所有必需文件是否存在
        for file_name in model_info["files"]:
            if not (model_dir / file_name).exists():
                return False
        
        return True
    
    def get_model_path(self, model_name: str) -> Optional[Path]:
        """获取模型路径"""
        if self.is_model_downloaded(model_name):
            return self.assets_dir / model_name
        return None
    
    def download_model_file(self, repo_id: str, filename: str, local_path: Path, model_name: str = None) -> bool:
        """下载单个模型文件（带重试和镜像支持）"""
        for attempt in range(self.max_retries):
            try:
                # 使用当前镜像
                mirror = self.get_current_mirror()
                url = f"{mirror}/{repo_id}/resolve/main/{filename}"
                
                print(f"尝试从 {mirror} 下载 {filename} (尝试 {attempt + 1}/{self.max_retries})")
                
                # 设置请求头，模拟浏览器
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                response = requests.get(url, stream=True, headers=headers, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                
                with open(local_path, 'wb') as f:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                                # 更新下载状态
                                if model_name:
                                    download_state_manager.update_file_progress(model_name, filename, pbar.n, total_size)
                                    # 通知监听器
                                    self._notify_progress(model_name, filename, pbar.n, total_size)
                
                print(f"✓ {filename} 下载成功")
                # 标记文件下载完成
                if model_name:
                    download_state_manager.complete_file(model_name, filename)
                return True
                
            except Exception as e:
                print(f"✗ 下载文件 {filename} 失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                
                # 记录错误
                if model_name:
                    download_state_manager.record_error(model_name, f"下载 {filename} 失败: {str(e)}")
                
                # 删除部分下载的文件
                if local_path.exists():
                    local_path.unlink()
                
                # 如果不是最后一次尝试，切换镜像并等待
                if attempt < self.max_retries - 1:
                    self.switch_mirror()
                    print(f"等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
        
        print(f"✗ {filename} 下载失败，已尝试所有镜像")
        return False
    
    def download_model(self, model_name: str) -> bool:
        """下载完整模型"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            print(f"不支持的模型: {model_name}")
            return False
        
        if self.is_model_downloaded(model_name):
            print(f"模型 {model_name} 已存在")
            # 清除可能存在的下载状态
            download_state_manager.clear_state(model_name)
            return True
        
        # 检查是否有未完成的下载
        if download_state_manager.is_downloading(model_name):
            print(f"检测到未完成的下载，尝试恢复...")
            return self._resume_download(model_name, model_info)
        
        # 重置镜像到第一个
        self.reset_mirror()
        
        model_dir = self.assets_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 开始新的下载
        all_files = model_info["files"] + model_info.get("optional_files", [])
        download_state_manager.start_download(model_name, len(model_info["files"]), all_files)
        # 通知状态变化
        self._notify_status(model_name, "downloading")
        
        print(f"开始下载模型: {model_info['description']}")
        print(f"预计大小: {model_info['size_mb']} MB")
        print(f"使用镜像: {self.get_current_mirror()}")
        
        success_count = 0
        total_files = len(model_info["files"])
        
        try:
            # 下载必需文件
            for i, filename in enumerate(model_info["files"]):
                local_path = model_dir / filename
                print(f"正在下载文件 {i+1}/{total_files}: {filename}")
                
                if self.download_model_file(model_info["repo_id"], filename, local_path, model_name):
                    success_count += 1
                else:
                    print(f"文件下载失败: {filename}")
                    download_state_manager.fail_download(model_name, f"必需文件 {filename} 下载失败")
                    # 清理已下载的文件
                    if model_dir.exists():
                        shutil.rmtree(model_dir)
                    return False
            
            # 下载可选文件（失败不影响整体下载）
            optional_files = model_info.get("optional_files", [])
            for filename in optional_files:
                local_path = model_dir / filename
                print(f"尝试下载可选文件: {filename}")
                if self.download_model_file(model_info["repo_id"], filename, local_path, model_name):
                    print(f"可选文件下载成功: {filename}")
                else:
                    print(f"可选文件下载失败（已忽略）: {filename}")
            
            if success_count == total_files:
                print(f"模型 {model_name} 下载完成！")
                download_state_manager.complete_download(model_name)
                # 通知状态变化
                self._notify_status(model_name, "completed")
                return True
            else:
                print(f"下载不完整: {success_count}/{total_files}")
                download_state_manager.fail_download(model_name, f"下载不完整: {success_count}/{total_files}")
                # 通知状态变化
                self._notify_status(model_name, "failed")
                if model_dir.exists():
                    shutil.rmtree(model_dir)
                return False
                
        except Exception as e:
            print(f"下载过程中出现异常: {e}")
            download_state_manager.fail_download(model_name, f"下载异常: {str(e)}")
            # 通知状态变化
            self._notify_status(model_name, "failed")
            if model_dir.exists():
                shutil.rmtree(model_dir)
            return False
    
    def _resume_download(self, model_name: str, model_info: Dict[str, Any]) -> bool:
        """恢复下载"""
        state = download_state_manager.get_download_state(model_name)
        if not state:
            return False
        
        model_dir = self.assets_dir / model_name
        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"恢复下载模型: {model_info['description']}")
        print(f"已完成文件: {state['completed_files']}/{state['total_files']}")
        
        # 重置镜像到第一个
        self.reset_mirror()
        
        success_count = state['completed_files']
        total_files = state['total_files']
        completed_files = set(state['completed_file_list'])
        
        try:
            # 下载未完成的必需文件
            for i, filename in enumerate(model_info["files"]):
                if filename in completed_files:
                    print(f"跳过已下载文件: {filename}")
                    continue
                
                local_path = model_dir / filename
                print(f"恢复下载文件 {i+1}/{total_files}: {filename}")
                
                if self.download_model_file(model_info["repo_id"], filename, local_path, model_name):
                    success_count += 1
                else:
                    print(f"文件下载失败: {filename}")
                    download_state_manager.fail_download(model_name, f"恢复下载时文件 {filename} 下载失败")
                    return False
            
            # 下载可选文件（如果之前没有完成）
            optional_files = model_info.get("optional_files", [])
            for filename in optional_files:
                if filename in completed_files:
                    print(f"跳过已下载的可选文件: {filename}")
                    continue
                
                local_path = model_dir / filename
                print(f"恢复下载可选文件: {filename}")
                if self.download_model_file(model_info["repo_id"], filename, local_path, model_name):
                    print(f"可选文件下载成功: {filename}")
                else:
                    print(f"可选文件下载失败（已忽略）: {filename}")
            
            if success_count == total_files:
                print(f"模型 {model_name} 恢复下载完成！")
                download_state_manager.complete_download(model_name)
                # 通知状态变化
                self._notify_status(model_name, "completed")
                return True
            else:
                print(f"恢复下载不完整: {success_count}/{total_files}")
                download_state_manager.fail_download(model_name, f"恢复下载不完整: {success_count}/{total_files}")
                # 通知状态变化
                self._notify_status(model_name, "failed")
                return False
                
        except Exception as e:
            print(f"恢复下载过程中出现异常: {e}")
            download_state_manager.fail_download(model_name, f"恢复下载异常: {str(e)}")
            # 通知状态变化
            self._notify_status(model_name, "failed")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """删除模型"""
        model_dir = self.assets_dir / model_name
        if model_dir.exists():
            shutil.rmtree(model_dir)
            print(f"模型 {model_name} 已删除")
            # 清除下载状态
            download_state_manager.clear_state(model_name)
            return True
        return False
    
    def get_downloaded_models(self) -> list:
        """获取已下载的模型列表"""
        downloaded = []
        for model_name in self.supported_models.keys():
            if self.is_model_downloaded(model_name):
                downloaded.append(model_name)
        return downloaded
    
    def get_model_size(self, model_name: str) -> int:
        """获取模型大小（字节）"""
        model_dir = self.assets_dir / model_name
        if not model_dir.exists():
            return 0
        
        total_size = 0
        for file_path in model_dir.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size
    
    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def get_download_progress(self, model_name: str) -> Dict[str, Any]:
        """获取下载进度信息"""
        return download_state_manager.get_progress_info(model_name)
    
    def is_downloading(self, model_name: str) -> bool:
        """检查是否正在下载"""
        return download_state_manager.is_downloading(model_name)
    
    def get_all_downloading_models(self) -> List[str]:
        """获取所有正在下载的模型"""
        return download_state_manager.get_all_downloading_models()
    
    # 监听器管理方法
    def subscribe_progress(self, model_name: str, callback: Callable[[str, int, int], None]):
        """订阅模型下载进度更新
        
        Args:
            model_name: 模型名称
            callback: 回调函数，参数为 (filename, downloaded, total)
        """
        if model_name not in self._progress_listeners:
            self._progress_listeners[model_name] = []
        
        if callback not in self._progress_listeners[model_name]:
            self._progress_listeners[model_name].append(callback)
            print(f"已订阅模型 {model_name} 的进度更新")
    
    def unsubscribe_progress(self, model_name: str, callback: Callable[[str, int, int], None]):
        """取消订阅模型下载进度更新
        
        Args:
            model_name: 模型名称
            callback: 要移除的回调函数
        """
        if model_name in self._progress_listeners:
            if callback in self._progress_listeners[model_name]:
                self._progress_listeners[model_name].remove(callback)
                print(f"已取消订阅模型 {model_name} 的进度更新")
                
                # 如果没有监听器了，删除该模型的监听器列表
                if not self._progress_listeners[model_name]:
                    del self._progress_listeners[model_name]
    
    def unsubscribe_all_progress(self, model_name: str):
        """取消订阅指定模型的所有进度更新
        
        Args:
            model_name: 模型名称
        """
        if model_name in self._progress_listeners:
            del self._progress_listeners[model_name]
            print(f"已取消订阅模型 {model_name} 的所有进度更新")
    
    def subscribe_status(self, callback: Callable[[str, str], None]):
        """订阅下载状态变化
        
        Args:
            callback: 回调函数，参数为 (model_name, status)
        """
        if callback not in self._status_listeners:
            self._status_listeners.append(callback)
            print("已订阅下载状态变化")
    
    def unsubscribe_status(self, callback: Callable[[str, str], None]):
        """取消订阅下载状态变化
        
        Args:
            callback: 要移除的回调函数
        """
        if callback in self._status_listeners:
            self._status_listeners.remove(callback)
            print("已取消订阅下载状态变化")
    
    def _notify_progress(self, model_name: str, filename: str, downloaded: int, total: int):
        """通知进度更新
        
        Args:
            model_name: 模型名称
            filename: 文件名
            downloaded: 已下载字节数
            total: 总字节数
        """
        if model_name in self._progress_listeners:
            for callback in self._progress_listeners[model_name]:
                try:
                    callback(filename, downloaded, total)
                except Exception as e:
                    print(f"进度监听器回调出错: {e}")
    
    def _notify_status(self, model_name: str, status: str):
        """通知状态变化
        
        Args:
            model_name: 模型名称
            status: 新状态
        """
        for callback in self._status_listeners:
            try:
                callback(model_name, status)
            except Exception as e:
                print(f"状态监听器回调出错: {e}")


# 全局模型管理器实例
model_manager = ModelManager()
