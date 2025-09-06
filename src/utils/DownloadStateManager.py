#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载状态管理器
负责跟踪和管理模型下载状态，支持进度恢复
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

class DownloadStateManager:
    def __init__(self, state_file: str = "download_state.json"):
        self.state_file = Path(state_file)
        self.state = {}  # 内存缓存
        self._load_state_from_disk()  # 从磁盘加载状态
    
    def _load_state_from_disk(self):
        """从磁盘加载下载状态到内存缓存"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        print("下载状态文件为空，使用空状态")
                        self.state = {}
                        return
                    
                    disk_state = json.loads(content)
                    
                    # 将磁盘状态加载到内存，并标记为暂停状态
                    for model_name, state in disk_state.items():
                        if state.get("status") == "downloading":
                            # 将正在下载的状态标记为暂停
                            state["status"] = "paused"
                            state["pause_time"] = datetime.now().isoformat()
                        
                        self.state[model_name] = state
                    
            except Exception as e:
                print(f"加载下载状态失败: {e}")
                # 如果文件损坏，尝试备份并重新创建
                try:
                    backup_file = self.state_file.with_suffix('.json.bak')
                    self.state_file.rename(backup_file)
                    print(f"已备份损坏的状态文件到: {backup_file}")
                except:
                    pass
                self.state = {}
        else:
            print("下载状态文件不存在，使用空状态")
            self.state = {}
    
    def _save_state(self):
        """保存下载状态到磁盘"""
        try:
            # 确保目录存在
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            
            # 验证写入是否成功
            if not (self.state_file.exists() and self.state_file.stat().st_size > 0):
                print(f"警告: 下载状态文件可能未正确保存")
                
        except Exception as e:
            print(f"保存下载状态到磁盘失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_memory_cache(self, model_name: str, updates: Dict[str, Any]):
        """更新内存缓存"""
        if model_name not in self.state:
            self.state[model_name] = {}
        
        self.state[model_name].update(updates)
    
    def start_download(self, model_name: str, total_files: int, files: List[str]):
        """开始下载"""
        download_info = {
            "status": "downloading",
            "start_time": datetime.now().isoformat(),
            "total_files": total_files,
            "completed_files": 0,
            "files": files,
            "completed_file_list": [],
            "current_file": None,
            "current_file_progress": 0,
            "current_file_total": 0,
            "error_count": 0,
            "last_error": None
        }
        self._update_memory_cache(model_name, download_info)
        self._save_state()
    
    def update_file_progress(self, model_name: str, filename: str, downloaded: int, total: int):
        """更新文件下载进度"""
        if model_name in self.state:
            progress_updates = {
                "current_file": filename,
                "current_file_progress": downloaded,
                "current_file_total": total
            }
            self._update_memory_cache(model_name, progress_updates)
            self._save_state()
    
    def complete_file(self, model_name: str, filename: str):
        """标记文件下载完成"""
        if model_name in self.state:
            if filename not in self.state[model_name]["completed_file_list"]:
                self.state[model_name]["completed_file_list"].append(filename)
                self.state[model_name]["completed_files"] += 1
            self.state[model_name]["current_file"] = None
            self.state[model_name]["current_file_progress"] = 0
            self.state[model_name]["current_file_total"] = 0
            self._save_state()
    
    def record_error(self, model_name: str, error_msg: str):
        """记录错误"""
        if model_name in self.state:
            self.state[model_name]["error_count"] += 1
            self.state[model_name]["last_error"] = error_msg
            self._save_state()
    
    def complete_download(self, model_name: str):
        """标记下载完成"""
        if model_name in self.state:
            self.state[model_name]["status"] = "completed"
            self.state[model_name]["end_time"] = datetime.now().isoformat()
            self._save_state()
    
    def fail_download(self, model_name: str, error_msg: str):
        """标记下载失败"""
        if model_name in self.state:
            self.state[model_name]["status"] = "failed"
            self.state[model_name]["end_time"] = datetime.now().isoformat()
            self.state[model_name]["last_error"] = error_msg
            self._save_state()
    
    def get_download_state(self, model_name: str) -> Optional[Dict[str, Any]]:
        """获取下载状态"""
        return self.state.get(model_name)
    
    def is_downloading(self, model_name: str) -> bool:
        """检查是否正在下载"""
        state = self.get_download_state(model_name)
        return state and state.get("status") == "downloading"
    
    def get_progress_info(self, model_name: str) -> Dict[str, Any]:
        """获取进度信息"""
        state = self.get_download_state(model_name)
        if not state:
            return {"progress": 0, "status": "not_started", "message": "未开始下载"}
        
        if state["status"] == "completed":
            return {"progress": 100, "status": "completed", "message": "下载完成"}
        
        if state["status"] == "failed":
            return {
                "progress": 0, 
                "status": "failed", 
                "message": f"下载失败: {state.get('last_error', '未知错误')}"
            }
        
        if state["status"] == "downloading":
            total_files = state["total_files"]
            completed_files = state["completed_files"]
            current_file = state.get("current_file")
            current_progress = state.get("current_file_progress", 0)
            current_total = state.get("current_file_total", 0)
            
            # 计算总体进度
            file_progress = (completed_files / total_files) * 100 if total_files > 0 else 0
            current_file_progress = (current_progress / current_total) * 100 if current_total > 0 else 0
            overall_progress = file_progress + (current_file_progress / total_files) if total_files > 0 else 0
            
            message = f"已下载 {completed_files}/{total_files} 个文件"
            if current_file:
                message += f"，正在下载: {current_file}"
                if current_total > 0:
                    message += f" ({current_progress/current_total*100:.1f}%)"
            
            return {
                "progress": min(overall_progress, 99.9),  # 避免显示100%直到真正完成
                "status": "downloading",
                "message": message,
                "current_file": current_file,
                "completed_files": completed_files,
                "total_files": total_files
            }
        
        return {"progress": 0, "status": "unknown", "message": "未知状态"}
    
    def clear_state(self, model_name: str):
        """清除下载状态"""
        if model_name in self.state:
            del self.state[model_name]
            self._save_state()
    
    def clear_all_states(self):
        """清除所有下载状态"""
        self.state = {}
        self._save_state()
    
    def get_all_downloading_models(self) -> List[str]:
        """获取所有正在下载的模型"""
        return [model_name for model_name, state in self.state.items() 
                if state.get("status") == "downloading"]
    
    def get_all_paused_models(self) -> List[str]:
        """获取所有暂停的模型"""
        return [model_name for model_name, state in self.state.items() 
                if state.get("status") == "paused"]
    
    def get_all_incomplete_models(self) -> List[str]:
        """获取所有未完成的模型（包括正在下载和暂停的）"""
        return [model_name for model_name, state in self.state.items() 
                if state.get("status") in ["downloading", "paused"]]
    
    def resume_download(self, model_name: str):
        """恢复下载（将暂停状态改为下载状态）"""
        if model_name in self.state and self.state[model_name].get("status") == "paused":
            resume_updates = {
                "status": "downloading",
                "resume_time": datetime.now().isoformat()
            }
            self._update_memory_cache(model_name, resume_updates)
            self._save_state()
            return True
        return False


# 全局下载状态管理器实例
download_state_manager = DownloadStateManager()
