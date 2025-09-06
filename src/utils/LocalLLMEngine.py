#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地LLM推理引擎
使用transformers库进行本地模型推理
"""

import os
import json
import torch
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("警告: transformers库未安装，本地LLM功能不可用")

from src.utils.ModelManager import model_manager

class LocalLLMEngine:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_name = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_loaded = False
        
    def load_model(self, model_name: str) -> bool:
        """加载本地模型"""
        if not TRANSFORMERS_AVAILABLE:
            print("错误: transformers库未安装")
            return False
        
        model_path = model_manager.get_model_path(model_name)
        if not model_path:
            print(f"错误: 模型 {model_name} 未下载")
            return False
        
        try:
            print(f"正在加载模型: {model_name}")
            print(f"使用设备: {self.device}")
            
            # 加载tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                str(model_path),
                trust_remote_code=True
            )
            
            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            self.model_name = model_name
            self.is_loaded = True
            
            print(f"模型 {model_name} 加载成功!")
            return True
            
        except Exception as e:
            print(f"加载模型失败: {e}")
            self.model = None
            self.tokenizer = None
            self.is_loaded = False
            return False
    
    def unload_model(self):
        """卸载模型释放内存"""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        self.is_loaded = False
        self.model_name = None
        
        # 清理GPU缓存
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def generate_response(self, messages: List[Dict[str, str]], max_length: int = 512, temperature: float = 0.7) -> str:
        """生成单次响应"""
        if not self.is_loaded:
            return "错误: 模型未加载"
        
        try:
            # 构建对话格式
            if self.model_name.startswith("qwen"):
                # Qwen模型使用特殊格式
                text = self._format_qwen_messages(messages)
            else:
                # 其他模型使用简单格式
                text = self._format_simple_messages(messages)
            
            # 编码输入
            inputs = self.tokenizer.encode(text, return_tensors="pt").to(self.device)
            
            # 生成响应
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # 解码响应
            response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
            return response.strip()
            
        except Exception as e:
            return f"生成响应时出错: {e}"
    
    def stream_response(self, messages: List[Dict[str, str]], callback: Callable[[str], None], 
                       error_callback: Optional[Callable[[str], None]] = None,
                       cancel_check: Optional[Callable[[], bool]] = None,
                       max_length: int = 512, temperature: float = 0.7):
        """流式生成响应"""
        if not self.is_loaded:
            if error_callback:
                error_callback("错误: 模型未加载")
            return
        
        try:
            # 构建对话格式
            if self.model_name.startswith("qwen"):
                text = self._format_qwen_messages(messages)
            else:
                text = self._format_simple_messages(messages)
            
            # 编码输入
            inputs = self.tokenizer.encode(text, return_tensors="pt").to(self.device)
            
            # 创建流式生成器
            class StreamCallback:
                def __init__(self, callback, cancel_check):
                    self.callback = callback
                    self.cancel_check = cancel_check
                    self.buffer = ""
                
                def __call__(self, token):
                    if self.cancel_check and self.cancel_check():
                        return False
                    
                    self.buffer += token
                    if token in ['。', '！', '？', '\n', '.', '!', '?'] or len(self.buffer) > 10:
                        if self.buffer.strip():
                            self.callback(self.buffer)
                            self.buffer = ""
                    return True
            
            stream_callback = StreamCallback(callback, cancel_check)
            
            # 生成响应
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    streamer=stream_callback
                )
            
            # 处理剩余的缓冲区内容
            if stream_callback.buffer.strip():
                callback(stream_callback.buffer)
                
        except Exception as e:
            if error_callback:
                error_callback(f"流式生成时出错: {e}")
    
    def _format_qwen_messages(self, messages: List[Dict[str, str]]) -> str:
        """格式化Qwen模型的消息"""
        formatted = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                formatted += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                formatted += f"<|im_start|>assistant\n{content}<|im_end|>\n"
        
        formatted += "<|im_start|>assistant\n"
        return formatted
    
    def _format_simple_messages(self, messages: List[Dict[str, str]]) -> str:
        """格式化简单模型的消息"""
        formatted = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                formatted += f"User: {content}\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n"
        
        formatted += "Assistant: "
        return formatted
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取当前模型信息"""
        if not self.is_loaded:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "model_name": self.model_name,
            "device": self.device,
            "model_size": model_manager.get_model_size(self.model_name) if self.model_name else 0
        }


# 全局本地LLM引擎实例
local_llm_engine = LocalLLMEngine()
