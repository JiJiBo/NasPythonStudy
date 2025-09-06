#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地LLM推理引擎
使用transformers库进行本地模型推理
"""

import os
import json
import torch
import logging
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("警告: transformers库未安装，本地LLM功能不可用")

from src.utils.ModelManager import model_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            print("错误: transformers库未安装，无法使用本地模型功能")
            return False
        
        model_path = model_manager.get_model_path(model_name)
        if not model_path:
            print(f"错误: 模型 {model_name} 未下载，请先下载模型")
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
                dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True,  # 减少内存消耗
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            self.model_name = model_name
            self.is_loaded = True
            
            print(f"模型 {model_name} 加载成功！")
            return True
            
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
            return "错误: 本地模型未加载"
        
        try:
            # 构建对话格式
            if self.model_name.startswith("qwen"):
                # Qwen模型使用特殊格式
                text = self._format_qwen_messages(messages)
            else:
                # 其他模型使用简单格式
                text = self._format_simple_messages(messages)
            
            # 编码输入 - 使用更现代的方式
            tokenized = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048,  # 设置合理的最大长度
                padding=False
            )
            inputs = tokenized["input_ids"].to(self.device)
            attention_mask = tokenized["attention_mask"].to(self.device)
            
            # 生成响应
            with torch.no_grad():
                # 计算可生成的新token数量，确保至少为1
                input_length = inputs.shape[1]
                available_tokens = max_length - input_length
                max_new_tokens = max(min(available_tokens, 512), 1)  # 确保至少为1
                
                outputs = self.model.generate(
                    inputs,
                    attention_mask=attention_mask,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # 解码响应
            response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
            # 调试日志：打印AI的原始输出
            logger.info(f"AI原始输出: {repr(response)}")
            return response.strip()
            
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
                       max_length: int = 512, temperature: float = 0.7):
        """流式生成响应"""
        if not self.is_loaded:
            if error_callback:
                error_callback("错误: 本地模型未加载")
            return
        
        try:
            # 构建对话格式
            if self.model_name.startswith("qwen"):
                text = self._format_qwen_messages(messages)
            else:
                text = self._format_simple_messages(messages)
            
            # 调试日志：打印格式化后的输入
            logger.info(f"格式化后的输入文本: {repr(text)}")
            
            # 编码输入 - 使用更现代的方式
            tokenized = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048,  # 设置合理的最大长度
                padding=False
            )
            inputs = tokenized["input_ids"].to(self.device)
            attention_mask = tokenized["attention_mask"].to(self.device)
            
            # 创建流式生成器
            class StreamCallback:
                def __init__(self, callback, cancel_check, tokenizer):
                    self.callback = callback
                    self.cancel_check = cancel_check
                    self.tokenizer = tokenizer
                    self.buffer = ""
                
                def put(self, token):
                    """TextStreamer 接口要求的方法"""
                    if self.cancel_check and self.cancel_check():
                        return False
                    
                    try:
                        # 处理不同类型的token输入
                        if hasattr(token, 'tolist'):  # 如果是Tensor
                            token_list = token.tolist()
                            if isinstance(token_list, list) and len(token_list) > 0:
                                if isinstance(token_list[0], list):  # 如果是二维列表 [[1,2,3]]
                                    token_list = token_list[0]
                                # 解码整个序列
                                token_text = self.tokenizer.decode(token_list, skip_special_tokens=True)
                                # 调试日志：打印解码后的token文本
                                logger.debug(f"解码后的token文本: {repr(token_text)}")
                            else:
                                return True
                        elif isinstance(token, (list, tuple)):  # 如果是列表或元组
                            token_text = self.tokenizer.decode(token, skip_special_tokens=True)
                        elif hasattr(token, 'item'):  # 如果是单元素Tensor
                            token_id = token.item()
                            token_text = self.tokenizer.decode([int(token_id)], skip_special_tokens=True)
                        else:  # 如果是标量
                            token_text = self.tokenizer.decode([int(token)], skip_special_tokens=True)
                        
                        # 只处理新生成的部分（排除输入部分）
                        if not hasattr(self, 'last_length'):
                            self.last_length = 0
                        
                        # 如果token_text比之前长，说明有新内容生成
                        if len(token_text) > self.last_length:
                            new_text = token_text[self.last_length:]
                            self.buffer += new_text
                            self.last_length = len(token_text)
                            
                            # 更智能的缓冲区输出策略
                            should_flush = False
                            
                            # 中文标点符号
                            if any(punct in new_text for punct in ['。', '！', '？', '；', '：']):
                                should_flush = True
                            # 英文标点符号和空格
                            elif any(punct in new_text for punct in ['.', '!', '?', ';', ':', '\n', ' ']):
                                should_flush = True
                            # 缓冲区长度限制
                            elif len(self.buffer) > 20:
                                should_flush = True
                            
                            if should_flush and self.buffer.strip():
                                # 调试日志：打印即将输出的缓冲区内容
                                logger.info(f"输出缓冲区内容: {repr(self.buffer)}")
                                self.callback(self.buffer)
                                self.buffer = ""
                        
                        return True
                    except Exception as e:
                        # 如果处理失败，跳过这个token
                        print(f"处理token时出错: {e}, token类型: {type(token)}, token形状: {getattr(token, 'shape', 'N/A')}")
                        return True
                
                def end(self):
                    """TextStreamer 接口要求的方法 - 生成结束时调用"""
                    # 输出剩余的缓冲区内容
                    if self.buffer.strip():
                        # 调试日志：打印最终输出的缓冲区内容
                        logger.info(f"最终输出缓冲区内容: {repr(self.buffer)}")
                        self.callback(self.buffer)
                        self.buffer = ""
                
                def __call__(self, token):
                    """保持向后兼容性"""
                    return self.put(token)
            
            stream_callback = StreamCallback(callback, cancel_check, self.tokenizer)
            
            # 生成响应
            with torch.no_grad():
                # 计算可生成的新token数量，确保至少为1
                input_length = inputs.shape[1]
                available_tokens = max_length - input_length
                max_new_tokens = max(min(available_tokens, 512), 1)  # 确保至少为1
                
                outputs = self.model.generate(
                    inputs,
                    attention_mask=attention_mask,
                    max_new_tokens=max_new_tokens,
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
            error_msg = f"流式生成时出错: {e}"
            logger.error(error_msg, exc_info=True)
            
            # 区分不同类型的错误
            if "CUDA out of memory" in str(e):
                error_msg += " (显存不足)"
            elif "tokenizer" in str(e).lower():
                error_msg += " (tokenizer解码错误)"
            elif "generate" in str(e).lower():
                error_msg += " (模型生成错误)"
            elif "stream" in str(e).lower():
                error_msg += " (流式处理错误)"
            
            if error_callback:
                error_callback(error_msg)
    
    def _format_qwen_messages(self, messages: List[Dict[str, str]]) -> str:
        """格式化Qwen模型的消息"""
        formatted = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                formatted += f"Human: {content}\n"
            elif role == "assistant":
                # 清理assistant消息中的污染标签
                clean_content = content.replace("user\n", "").replace("assistant\n", "").replace("User:", "").replace("Assistant:", "").strip()
                formatted += f"Assistant: {clean_content}\n"
        
        formatted += "Assistant: "
        logger.debug(f"Qwen消息格式化结果: {repr(formatted)}")
        return formatted
    
    def _format_simple_messages(self, messages: List[Dict[str, str]]) -> str:
        """格式化简单模型的消息"""
        formatted = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                formatted += f"Q: {content}\n"
            elif role == "assistant":
                # 清理assistant消息中的污染标签
                clean_content = content.replace("user\n", "").replace("assistant\n", "").replace("User:", "").replace("Assistant:", "").strip()
                formatted += f"A: {clean_content}\n"
        
        formatted += "A: "
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
        if self.device == "cuda" and torch.cuda.is_available():
            info.update({
                "gpu_memory_allocated": torch.cuda.memory_allocated(),
                "gpu_memory_reserved": torch.cuda.memory_reserved(),
                "gpu_memory_max_allocated": torch.cuda.max_memory_allocated()
            })
        
        return info


# 全局本地LLM引擎实例
local_llm_engine = LocalLLMEngine()
