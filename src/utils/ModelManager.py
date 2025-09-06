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
from typing import Optional, Dict, Any
import requests
from tqdm import tqdm

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
    
    def download_model_file(self, repo_id: str, filename: str, local_path: Path, progress_callback=None) -> bool:
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
                    if progress_callback:
                        with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    pbar.update(len(chunk))
                                    if progress_callback:
                                        progress_callback(filename, pbar.n, total_size)
                    else:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                
                print(f"✓ {filename} 下载成功")
                return True
                
            except Exception as e:
                print(f"✗ 下载文件 {filename} 失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                
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
    
    def download_model(self, model_name: str, progress_callback=None) -> bool:
        """下载完整模型"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            print(f"不支持的模型: {model_name}")
            return False
        
        if self.is_model_downloaded(model_name):
            print(f"模型 {model_name} 已存在")
            return True
        
        # 重置镜像到第一个
        self.reset_mirror()
        
        model_dir = self.assets_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"开始下载模型: {model_info['description']}")
        print(f"预计大小: {model_info['size_mb']} MB")
        print(f"使用镜像: {self.get_current_mirror()}")
        
        success_count = 0
        total_files = len(model_info["files"])
        
        # 下载必需文件
        for i, filename in enumerate(model_info["files"]):
            local_path = model_dir / filename
            print(f"正在下载文件 {i+1}/{total_files}: {filename}")
            
            if self.download_model_file(model_info["repo_id"], filename, local_path, progress_callback):
                success_count += 1
            else:
                print(f"文件下载失败: {filename}")
                # 清理已下载的文件
                if model_dir.exists():
                    shutil.rmtree(model_dir)
                return False
        
        # 下载可选文件（失败不影响整体下载）
        optional_files = model_info.get("optional_files", [])
        for filename in optional_files:
            local_path = model_dir / filename
            print(f"尝试下载可选文件: {filename}")
            if self.download_model_file(model_info["repo_id"], filename, local_path, progress_callback):
                print(f"可选文件下载成功: {filename}")
            else:
                print(f"可选文件下载失败（已忽略）: {filename}")
        
        if success_count == total_files:
            print(f"模型 {model_name} 下载完成！")
            return True
        else:
            print(f"下载不完整: {success_count}/{total_files}")
            if model_dir.exists():
                shutil.rmtree(model_dir)
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """删除模型"""
        model_dir = self.assets_dir / model_name
        if model_dir.exists():
            shutil.rmtree(model_dir)
            print(f"模型 {model_name} 已删除")
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


# 全局模型管理器实例
model_manager = ModelManager()
