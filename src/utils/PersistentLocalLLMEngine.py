#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持久化本地LLM推理引擎
使用长驻模型服务，避免重复加载模型
"""

import os
import json
import sys
import logging
import subprocess
import threading
import time
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

from src.utils.ModelManager import model_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersistentLocalLLMEngine:
    def __init__(self):
        self.model_name = None
        self.device = "cpu"
        self.is_loaded = False
        self.python_exe = None
        self.model_service_process = None
        self.model_service_stdin = None
        self.model_service_stdout = None
        self.request_id_counter = 0
        self.pending_requests = {}
        self.response_thread = None
        self.is_service_ready = False
        
        # 设置python_env的Python可执行文件路径
        python_env_path = Path(__file__).parent.parent.parent / "python_env"
        if python_env_path.exists():
            self.python_exe = python_env_path / "python.exe"
        
        # 检查torch是否可用
        if self.python_exe:
            self._check_cuda_availability()
    
    def _check_cuda_availability(self):
        """检查CUDA可用性"""
        try:
            result = subprocess.run([
                str(self.python_exe), "-c", 
                "import torch; print(f'cuda_available:{torch.cuda.is_available()}'); print(f'cuda_version:{torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'gpu_count:{torch.cuda.device_count() if torch.cuda.is_available() else 0}')"
            ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
            
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        if key == 'cuda_available':
                            if value == 'True':
                                self.device = "cuda"
                                print(f"✅ 使用独立Python环境中的torch，设备: {self.device}")
                            else:
                                self.device = "cpu"
                                print(f"✅ 使用独立Python环境中的torch，设备: {self.device}")
                        elif key == 'cuda_version' and self.device == "cuda":
                            print(f"CUDA版本: {value}")
                        elif key == 'gpu_count' and self.device == "cuda":
                            print(f"GPU数量: {value}")
        except Exception as e:
            print(f"检查torch设备时出错: {e}")
            self.device = "cpu"
    
    def _start_model_service(self, model_path):
        """启动模型服务"""
        try:
            service_script = Path(__file__).parent.parent.parent / "python_env" / "model_service.py"
            
            if not self.python_exe.exists() or not service_script.exists():
                return False
            
            # 启动模型服务进程
            self.model_service_process = subprocess.Popen([
                str(self.python_exe), str(service_script), str(model_path), self.device
            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', errors='replace', bufsize=1)
            
            self.model_service_stdin = self.model_service_process.stdin
            self.model_service_stdout = self.model_service_process.stdout
            
            # 启动响应处理线程
            self.response_thread = threading.Thread(target=self._handle_responses)
            self.response_thread.daemon = True
            self.response_thread.start()
            
            # 等待服务就绪
            start_time = time.time()
            while not self.is_service_ready and time.time() - start_time < 60:
                time.sleep(0.1)
            
            if self.is_service_ready:
                print("✅ 模型服务启动成功")
                return True
            else:
                print("❌ 模型服务启动超时")
                return False
                
        except Exception as e:
            print(f"启动模型服务时出错: {e}")
            return False
    
    def _handle_responses(self):
        """处理模型服务的响应"""
        try:
            while True:
                line = self.model_service_stdout.readline()
                if not line:
                    break
                
                line = line.strip()
                if line == "MODEL_SERVICE_READY":
                    self.is_service_ready = True
                    continue
                
                if line.startswith("RESPONSE: "):
                    try:
                        response_data = json.loads(line[10:])
                        request_id = response_data.get("request_id")
                        if request_id in self.pending_requests:
                            self.pending_requests[request_id]["response"] = response_data["content"]
                            self.pending_requests[request_id]["event"].set()
                    except json.JSONDecodeError:
                        pass
                
                elif line.startswith("STREAM_CHUNK: "):
                    try:
                        chunk_data = json.loads(line[14:])
                        request_id = chunk_data.get("request_id")
                        if request_id in self.pending_requests:
                            callback = self.pending_requests[request_id].get("callback")
                            if callback:
                                callback(chunk_data["content"])
                    except json.JSONDecodeError:
                        pass
                
                elif line.startswith("STREAM_END: "):
                    try:
                        end_data = json.loads(line[12:])
                        request_id = end_data.get("request_id")
                        if request_id in self.pending_requests:
                            self.pending_requests[request_id]["event"].set()
                    except json.JSONDecodeError:
                        pass
                
                elif line.startswith("ERROR: "):
                    try:
                        error_data = json.loads(line[7:])
                        request_id = error_data.get("request_id")
                        if request_id in self.pending_requests:
                            self.pending_requests[request_id]["error"] = error_data["message"]
                            self.pending_requests[request_id]["event"].set()
                    except json.JSONDecodeError:
                        pass
                        
        except Exception as e:
            logger.error(f"处理响应时出错: {e}")
    
    def load_model(self, model_name: str) -> bool:
        """加载本地模型"""
        model_path = model_manager.get_model_path(model_name)
        if not model_path:
            print(f"错误: 模型 {model_name} 未下载，请先下载模型")
            return False
        
        try:
            print(f"正在启动模型服务: {model_name}")
            print(f"使用设备: {self.device}")
            
            if self._start_model_service(model_path):
                self.model_name = model_name
                self.is_loaded = True
                print(f"✅ 模型 {model_name} 服务启动成功")
                return True
            else:
                print(f"❌ 模型 {model_name} 服务启动失败")
                return False
                
        except Exception as e:
            error_msg = f"启动模型服务失败: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
            return False
    
    def unload_model(self):
        """卸载模型释放内存"""
        if self.model_service_process:
            try:
                # 发送关闭命令
                shutdown_cmd = json.dumps({"type": "shutdown"})
                self.model_service_stdin.write(shutdown_cmd + "\n")
                self.model_service_stdin.flush()
                
                # 等待进程结束
                self.model_service_process.wait(timeout=10)
            except Exception as e:
                print(f"关闭模型服务时出错: {e}")
                if self.model_service_process:
                    self.model_service_process.terminate()
            finally:
                self.model_service_process = None
                self.model_service_stdin = None
                self.model_service_stdout = None
                self.is_service_ready = False
        
        self.is_loaded = False
        self.model_name = None
    
    def generate_response(self, messages: List[Dict[str, str]], max_length: int = 2048, temperature: float = 0.7) -> str:
        """生成单次响应"""
        if not self.is_loaded:
            return "错误: 本地模型未加载"
        
        try:
            request_id = str(self.request_id_counter)
            self.request_id_counter += 1
            
            # 创建请求
            request = {
                "type": "generate",
                "request_id": request_id,
                "messages": messages,
                "max_length": max_length,
                "temperature": temperature
            }
            
            # 设置等待事件
            event = threading.Event()
            self.pending_requests[request_id] = {
                "event": event,
                "response": None,
                "error": None
            }
            
            # 发送请求
            request_json = json.dumps(request, ensure_ascii=False)
            self.model_service_stdin.write(request_json + "\n")
            self.model_service_stdin.flush()
            
            # 等待响应
            if event.wait(timeout=60):
                if request_id in self.pending_requests:
                    if self.pending_requests[request_id]["error"]:
                        return f"推理失败: {self.pending_requests[request_id]['error']}"
                    else:
                        response = self.pending_requests[request_id]["response"]
                        logger.info(f"AI原始输出: {repr(response)}")
                        return response
            else:
                return "推理超时"
            
        except Exception as e:
            error_msg = f"生成响应时出错: {e}"
            logger.error(error_msg, exc_info=True)
            return error_msg
        finally:
            # 清理请求记录
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
    
    def stream_response(self, messages: List[Dict[str, str]], callback: Callable[[str], None], 
                       error_callback: Optional[Callable[[str], None]] = None,
                       cancel_check: Optional[Callable[[], bool]] = None,
                       max_length: int = 2048, temperature: float = 0.7):
        """流式生成响应"""
        if not self.is_loaded:
            if error_callback:
                error_callback("错误: 本地模型未加载")
            return
        
        try:
            request_id = str(self.request_id_counter)
            self.request_id_counter += 1
            
            # 创建请求
            request = {
                "type": "stream",
                "request_id": request_id,
                "messages": messages,
                "max_length": max_length,
                "temperature": temperature
            }
            
            # 设置等待事件
            event = threading.Event()
            self.pending_requests[request_id] = {
                "event": event,
                "callback": callback,
                "error": None
            }
            
            # 发送请求
            request_json = json.dumps(request, ensure_ascii=False)
            self.model_service_stdin.write(request_json + "\n")
            self.model_service_stdin.flush()
            
            # 等待流式响应完成
            if event.wait(timeout=120):
                if request_id in self.pending_requests and self.pending_requests[request_id]["error"]:
                    if error_callback:
                        error_callback(f"流式推理失败: {self.pending_requests[request_id]['error']}")
            else:
                if error_callback:
                    error_callback("流式推理超时")
            
        except Exception as e:
            error_msg = f"流式生成时出错: {e}"
            logger.error(error_msg, exc_info=True)
            if error_callback:
                error_callback(error_msg)
        finally:
            # 清理请求记录
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取当前模型信息"""
        if not self.is_loaded:
            return {"loaded": False}
        
        info = {
            "loaded": True,
            "model_name": self.model_name,
            "device": self.device,
            "model_size": model_manager.get_model_size(self.model_name) if self.model_name else 0,
            "service_ready": self.is_service_ready
        }
        
        return info

# 全局持久化本地LLM引擎实例
persistent_local_llm_engine = PersistentLocalLLMEngine()
