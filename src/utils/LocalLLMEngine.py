#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地LLM推理引擎
使用transformers库进行本地模型推理
"""

import os
import json
import sys
import logging
import subprocess
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

# 注意：由于DLL冲突，我们不能直接导入python_env中的torch和transformers
# 而是通过subprocess调用python_env中的Python来执行相关操作
# 库的可用性检查将在类初始化时进行

from src.utils.ModelManager import model_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalLLMEngine:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_name = None
        self.device = "cpu"  # 默认使用CPU
        self.is_loaded = False
        self.python_exe = None
        self.torch_available = False
        self.transformers_available = False
        
        # 设置python_env的Python可执行文件路径
        python_env_path = Path(__file__).parent.parent.parent / "python_env"
        if python_env_path.exists():
            self.python_exe = python_env_path / "python.exe"
        
        # 检查torch和transformers是否可用
        if self.python_exe:
            self._check_libraries_availability()
        
        # 检查torch是否可用
        if self.torch_available and self.python_exe:
            try:
                # 通过subprocess检查CUDA可用性
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
                else:
                    print(f"检查torch设备时出错: {result.stderr}")
                    self.device = "cpu"
            except Exception as e:
                print(f"检查torch设备时出错: {e}")
                self.device = "cpu"
        else:
            print("警告: torch不可用，将使用CPU模式")
    
    def _check_libraries_availability(self):
        """检查torch和transformers库的可用性"""
        try:
            print("正在检查torch库可用性...")
            # 检查torch是否可用 - 增加超时时间到30秒
            result = subprocess.run([
                str(self.python_exe), "-c", "import torch; print('torch_available')"
            ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
            if result.returncode == 0 and result.stdout and "torch_available" in result.stdout:
                self.torch_available = True
                print("✅ 检测到python_env中的torch库")
            else:
                print("警告: python_env中torch库未安装，本地LLM功能不可用")
            
            if self.torch_available:
                print("正在检查transformers库可用性...")
                # 检查transformers是否可用
                result = subprocess.run([
                    str(self.python_exe), "-c", "from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer; print('transformers_available')"
                ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
                if result.returncode == 0 and result.stdout and "transformers_available" in result.stdout:
                    self.transformers_available = True
                    print("✅ 检测到python_env中的transformers库")
                else:
                    print("警告: python_env中transformers库未安装，本地LLM功能不可用")
                
        except subprocess.TimeoutExpired:
            print("警告: 库检查超时，可能是首次导入torch需要较长时间")
            # 即使超时，也假设库是可用的，让后续使用来验证
            self.torch_available = True
            self.transformers_available = True
        except Exception as e:
            print(f"检查python_env库时出错: {e}")
        
    def load_model(self, model_name: str) -> bool:
        """加载本地模型"""
        if not self.torch_available:
            print("错误: torch库未安装，无法使用本地模型功能")
            return False
            
        if not self.transformers_available:
            print("错误: transformers库未安装，无法使用本地模型功能")
            return False
        
        model_path = model_manager.get_model_path(model_name)
        if not model_path:
            print(f"错误: 模型 {model_name} 未下载，请先下载模型")
            return False
        
        try:
            print(f"正在加载模型: {model_name}")
            print(f"使用设备: {self.device}")
            
            # 通过subprocess调用python_env中的Python来加载模型
            python_env_path = Path(__file__).parent.parent.parent / "python_env"
            python_exe = python_env_path / "python.exe"
            if not python_exe.exists():
                print("错误: python_env/python.exe不存在")
                return False
            
            # 创建模型加载脚本
            load_script = f"""
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

model_path = r"{model_path}"
device = "{self.device}"

try:
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None,
        low_cpu_mem_usage=True,
        trust_remote_code=True
    )
    
    if device == "cpu":
        model = model.to("cpu")
    
    print("MODEL_LOADED_SUCCESS")
    print(f"模型 {model_path} 加载成功")
    
except Exception as e:
    print(f"MODEL_LOAD_ERROR: {{e}}")
    sys.exit(1)
"""
            
            # 执行模型加载
            result = subprocess.run([
                str(python_exe), "-c", load_script
            ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)  # 5分钟超时
            
            if result.returncode == 0 and result.stdout and "MODEL_LOADED_SUCCESS" in result.stdout:
                self.model_name = model_name
                self.is_loaded = True
                print(f"✅ 模型 {model_name} 加载成功")
                return True
            else:
                error_msg = result.stderr or result.stdout
                print(f"模型加载失败: {error_msg}")
                return False
            
        except Exception as e:
            error_msg = f"加载模型失败: {e}"
            logger.error(error_msg, exc_info=True)
            
            # 区分不同类型的错误
            if "CUDA out of memory" in str(e):
                error_msg += " (显存不足，请尝试使用CPU或减少模型大小)"
            elif "No such file or directory" in str(e):
                error_msg += " (模型文件不存在，请检查模型路径)"
            elif "transformers" in str(e).lower():
                error_msg += " (transformers库相关错误)"
            
            print(error_msg)
            self.model = None
            self.tokenizer = None
            self.is_loaded = False
            return False
    
    def unload_model(self):
        """卸载模型释放内存"""
        # 由于我们使用subprocess，模型在独立进程中，这里只需要重置状态
        self.is_loaded = False
        self.model_name = None
        
        # 清理GPU缓存（通过subprocess调用）
        try:
            python_env_path = Path(__file__).parent.parent.parent / "python_env"
            python_exe = python_env_path / "python.exe"
            if python_exe.exists():
                subprocess.run([
                    str(python_exe), "-c", 
                    "import torch; torch.cuda.empty_cache() if torch.cuda.is_available() else None"
                ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=10)
        except Exception as e:
            print(f"清理GPU缓存时出错: {e}")
    
    def generate_response(self, messages: List[Dict[str, str]], max_length: int = 2048, temperature: float = 0.7) -> str:
        """生成单次响应"""
        if not self.is_loaded:
            return "错误: 本地模型未加载"
        
        try:
            # 通过subprocess调用python_env中的模型推理脚本
            python_env_path = Path(__file__).parent.parent.parent / "python_env"
            python_exe = python_env_path / "python.exe"
            inference_script = python_env_path / "model_inference.py"
            
            if not python_exe.exists() or not inference_script.exists():
                return "错误: 模型推理脚本不存在"
            
            # 获取模型路径
            from src.utils.ModelManager import model_manager
            model_path = model_manager.get_model_path(self.model_name)
            if not model_path:
                return "错误: 模型路径不存在"
            
            # 准备消息数据
            messages_json = json.dumps(messages, ensure_ascii=False)
            
            # 执行推理
            result = subprocess.run([
                str(python_exe), str(inference_script), "generate",
                str(model_path), messages_json, str(max_length), str(temperature), self.device
            ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120, bufsize=65536)
            
            if result.returncode == 0 and result.stdout:
                output = result.stdout.strip()
                if output.startswith("RESPONSE_SUCCESS: "):
                    response = output[19:]  # 移除前缀 "RESPONSE_SUCCESS: "
                    logger.info(f"AI原始输出: {repr(response)}")
                    return response.strip()
                elif output.startswith("RESPONSE_ERROR: "):
                    return output[17:]  # 移除前缀 "RESPONSE_ERROR: "
                else:
                    return output
            else:
                error_msg = result.stderr if result.stderr else (result.stdout if result.stdout else "未知错误")
                return f"推理失败: {error_msg}"
            
        except Exception as e:
            error_msg = f"生成响应时出错: {e}"
            logger.error(error_msg, exc_info=True)
            
            # 区分不同类型的错误
            if "CUDA out of memory" in str(e):
                error_msg += " (显存不足)"
            elif "tokenizer" in str(e).lower():
                error_msg += " (tokenizer解码错误)"
            elif "generate" in str(e).lower():
                error_msg += " (模型生成错误)"
            
            return error_msg
    
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
            # 通过subprocess调用python_env中的模型推理脚本进行流式推理
            python_env_path = Path(__file__).parent.parent.parent / "python_env"
            python_exe = python_env_path / "python.exe"
            inference_script = python_env_path / "model_inference.py"
            
            if not python_exe.exists() or not inference_script.exists():
                if error_callback:
                    error_callback("错误: 模型推理脚本不存在")
                return
            
            # 获取模型路径
            from src.utils.ModelManager import model_manager
            model_path = model_manager.get_model_path(self.model_name)
            if not model_path:
                if error_callback:
                    error_callback("错误: 模型路径不存在")
                return
            
            # 准备消息数据
            messages_json = json.dumps(messages, ensure_ascii=False)
            
            # 执行流式推理
            process = subprocess.Popen([
                str(python_exe), str(inference_script), "generate",
                str(model_path), messages_json, str(max_length), str(temperature), self.device
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', bufsize=1)
            
            # 实时读取输出
            while True:
                if cancel_check and cancel_check():
                    process.terminate()
                    break
                    
                line = process.stdout.readline()
                if not line:
                    break
                    
                line = line.strip()
                if line.startswith("STREAM_CHUNK: "):
                    chunk = line[14:]  # 移除前缀
                    callback(chunk)
                elif line.startswith("RESPONSE_ERROR: "):
                    if error_callback:
                        error_callback(line[16:])
                    break
            
            process.wait()
            
        except Exception as e:
            error_msg = f"流式生成时出错: {e}"
            logger.error(error_msg, exc_info=True)
            
            if error_callback:
                error_callback(error_msg)
    
    def _format_qwen_messages(self, messages: List[Dict[str, str]]) -> str:
        """格式化Qwen模型的消息"""
        # 只取最后一条用户消息
        user_message = None
        for message in reversed(messages):
            if message["role"] == "user":
                user_message = message["content"]
                break
        
        if user_message is None:
            return ""
        
        # 清理用户消息中的污染标签
        clean_content = user_message.replace("user\n", "").replace("assistant\n", "").replace("User:", "").replace("Assistant:", "").replace("Human:", "").replace("用户：", "").replace("助手：", "").replace("问：", "").replace("答：", "").strip()
        
        # 使用更自然的提示词格式
        formatted = f"请回答以下问题：{clean_content}\n回答："
        
        logger.debug(f"Qwen消息格式化结果: {repr(formatted)}")
        return formatted
    
    def _format_simple_messages(self, messages: List[Dict[str, str]]) -> str:
        """格式化简单模型的消息"""
        # 只取最后一条用户消息
        user_message = None
        for message in reversed(messages):
            if message["role"] == "user":
                user_message = message["content"]
                break
        
        if user_message is None:
            return ""
        
        # 清理用户消息中的污染标签
        clean_content = user_message.replace("user\n", "").replace("assistant\n", "").replace("User:", "").replace("Assistant:", "").replace("Human:", "").replace("用户：", "").replace("助手：", "").replace("问：", "").replace("答：", "").replace("Q:", "").replace("A:", "").strip()
        
        # 使用更自然的提示词格式
        formatted = f"请回答以下问题：{clean_content}\n回答："
        
        logger.debug(f"简单消息格式化结果: {repr(formatted)}")
        return formatted
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取当前模型信息"""
        if not self.is_loaded:
            return {"loaded": False}
        
        info = {
            "loaded": True,
            "model_name": self.model_name,
            "device": self.device,
            "model_size": model_manager.get_model_size(self.model_name) if self.model_name else 0
        }
        
        # 添加更多模型信息
        if self.model and hasattr(self.model, 'config'):
            config = self.model.config
            info.update({
                "max_position_embeddings": getattr(config, 'max_position_embeddings', None),
                "hidden_size": getattr(config, 'hidden_size', None),
                "num_attention_heads": getattr(config, 'num_attention_heads', None),
                "num_layers": getattr(config, 'num_hidden_layers', None),
                "vocab_size": getattr(config, 'vocab_size', None)
            })
        
        # 添加显存使用信息
        if self.torch_available and self.device == "cuda":
            try:
                # 通过subprocess获取GPU内存信息
                python_env_path = Path(__file__).parent.parent.parent / "python_env"
                python_exe = python_env_path / "python.exe"
                if python_exe.exists():
                    result = subprocess.run([
                        str(python_exe), "-c", 
                        "import torch; print(f'gpu_memory_allocated:{torch.cuda.memory_allocated()}'); print(f'gpu_memory_reserved:{torch.cuda.memory_reserved()}'); print(f'gpu_memory_max_allocated:{torch.cuda.max_memory_allocated()}')"
                    ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=10)
                    
                    if result.returncode == 0 and result.stdout:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if ':' in line:
                                key, value = line.split(':', 1)
                                if key == 'gpu_memory_allocated':
                                    info["gpu_memory_allocated"] = int(value)
                                elif key == 'gpu_memory_reserved':
                                    info["gpu_memory_reserved"] = int(value)
                                elif key == 'gpu_memory_max_allocated':
                                    info["gpu_memory_max_allocated"] = int(value)
            except Exception as e:
                logger.warning(f"获取GPU内存信息时出错: {e}")
        
        return info


# 全局本地LLM引擎实例
local_llm_engine = LocalLLMEngine()
