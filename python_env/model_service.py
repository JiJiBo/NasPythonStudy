#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长驻模型服务
使用multiprocessing实现模型常驻内存，避免重复加载
"""

import sys
import json
import time
import queue
import threading
import multiprocessing as mp
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer

# 设置标准输出编码
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

class ModelService:
    def __init__(self, model_path, device="cuda"):
        self.model_path = model_path
        self.device = device
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        
    def load_model(self):
        """加载模型和tokenizer"""
        try:
            print(f"正在加载模型: {self.model_path}", file=sys.stderr)
            print(f"使用设备: {self.device}", file=sys.stderr)
            
            # 加载tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to("cpu")
            
            self.is_loaded = True
            print("MODEL_LOADED_SUCCESS", file=sys.stderr)
            return True
            
        except Exception as e:
            print(f"MODEL_LOAD_ERROR: {e}", file=sys.stderr)
            return False
    
    def format_messages(self, messages):
        """格式化消息"""
        if not messages or not isinstance(messages, list):
            return ""
        
        formatted_text = ""
        for message in messages:
            if not isinstance(message, dict):
                continue
            role = message.get("role", "")
            content = message.get("content", "")
            if not content:
                continue
                
            if role == "user":
                formatted_text += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                formatted_text += f"<|im_start|>assistant\n{content}<|im_end|>\n"
        
        formatted_text += "<|im_start|>assistant\n"
        return formatted_text
    
    def generate_response(self, messages, max_length=2048, temperature=0.7):
        """生成响应"""
        if not self.is_loaded:
            return "MODEL_NOT_LOADED"
        
        try:
            # 格式化消息
            text = self.format_messages(messages)
            if not text:
                return "EMPTY_MESSAGE"
            
            print(f"DEBUG: formatted text length: {len(text)}", file=sys.stderr)
            
            # 编码输入
            tokenized = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048,
                padding=False
            )
            inputs = tokenized["input_ids"].to(self.device)
            attention_mask = tokenized["attention_mask"].to(self.device)
            
            # 计算max_new_tokens
            input_length = inputs.shape[1]
            max_new_tokens = max(200, min(max_length - input_length, 1024))
            
            # 生成响应
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    attention_mask=attention_mask,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # 解码响应
            response_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(response_tokens, skip_special_tokens=True)
            
            # 清理响应
            response = response.strip()
            
            # 移除ANSI转义序列
            import re
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            response = ansi_escape.sub('', response)
            
            # 移除各种前缀和后缀
            if response.startswith("助手: "):
                response = response[3:]
            if response.startswith("Assistant: "):
                response = response[11:]
            if response.startswith("<|im_start|>assistant\n"):
                response = response[21:]
            if response.startswith("<|im_end|>"):
                response = response[10:]
            if response.endswith("<|im_end|>"):
                response = response[:-10]
            if response.endswith("<|im_start|>"):
                response = response[:-12]
            
            response = response.strip()
            return response
            
        except Exception as e:
            return f"GENERATION_ERROR: {e}"
    
    def stream_response(self, messages, max_length=2048, temperature=0.7):
        """流式生成响应"""
        if not self.is_loaded:
            yield "MODEL_NOT_LOADED"
            return
        
        try:
            # 格式化消息
            text = self.format_messages(messages)
            if not text:
                yield "EMPTY_MESSAGE"
                return
            
            print(f"DEBUG: stream formatted text length: {len(text)}", file=sys.stderr)
            
            # 编码输入
            tokenized = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048,
                padding=False
            )
            inputs = tokenized["input_ids"].to(self.device)
            attention_mask = tokenized["attention_mask"].to(self.device)
            
            # 计算max_new_tokens
            input_length = inputs.shape[1]
            max_new_tokens = max(200, min(max_length - input_length, 1024))
            
            # 创建流式输出器
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
            
            # 在单独线程中生成
            generation_kwargs = {
                "input_ids": inputs,
                "attention_mask": attention_mask,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "do_sample": True,
                "pad_token_id": self.tokenizer.eos_token_id,
                "eos_token_id": self.tokenizer.eos_token_id,
                "repetition_penalty": 1.1,
                "streamer": streamer
            }
            
            thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            
            # 流式输出响应
            for new_text in streamer:
                # 清理文本
                import re
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                clean_text = ansi_escape.sub('', new_text)
                yield clean_text
            
            thread.join()
            
        except Exception as e:
            yield f"STREAM_ERROR: {e}"

def model_worker(request_queue, response_queue, model_path, device):
    """模型工作进程"""
    service = ModelService(model_path, device)
    
    # 加载模型
    if not service.load_model():
        response_queue.put({"type": "error", "message": "模型加载失败"})
        return
    
    response_queue.put({"type": "ready", "message": "模型服务已就绪"})
    
    # 处理请求
    while True:
        try:
            request = request_queue.get(timeout=1)
            if request is None:  # 退出信号
                break
            
            request_type = request.get("type")
            
            if request_type == "generate":
                messages = request.get("messages", [])
                max_length = request.get("max_length", 2048)
                temperature = request.get("temperature", 0.7)
                
                response = service.generate_response(messages, max_length, temperature)
                response_queue.put({
                    "type": "response",
                    "request_id": request.get("request_id"),
                    "content": response
                })
            
            elif request_type == "stream":
                messages = request.get("messages", [])
                max_length = request.get("max_length", 2048)
                temperature = request.get("temperature", 0.7)
                request_id = request.get("request_id")
                
                for chunk in service.stream_response(messages, max_length, temperature):
                    response_queue.put({
                        "type": "stream_chunk",
                        "request_id": request_id,
                        "content": chunk
                    })
                
                response_queue.put({
                    "type": "stream_end",
                    "request_id": request_id
                })
            
            elif request_type == "shutdown":
                break
                
        except queue.Empty:
            continue
        except Exception as e:
            response_queue.put({
                "type": "error",
                "message": f"处理请求时出错: {e}"
            })

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python model_service.py <model_path> <device>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    device = sys.argv[2]
    
    # 创建队列
    request_queue = mp.Queue()
    response_queue = mp.Queue()
    
    # 启动模型工作进程
    process = mp.Process(
        target=model_worker,
        args=(request_queue, response_queue, model_path, device)
    )
    process.start()
    
    # 等待模型加载完成
    while True:
        try:
            response = response_queue.get(timeout=30)
            if response["type"] == "ready":
                print("MODEL_SERVICE_READY")
                break
            elif response["type"] == "error":
                print(f"MODEL_SERVICE_ERROR: {response['message']}")
                sys.exit(1)
        except queue.Empty:
            print("MODEL_SERVICE_TIMEOUT")
            sys.exit(1)
    
    # 处理标准输入的命令
    try:
        while True:
            line = input()
            if not line:
                continue
            
            try:
                command = json.loads(line)
                request_queue.put(command)
                
                # 等待响应
                while True:
                    response = response_queue.get(timeout=60)
                    
                    if response["type"] == "response":
                        print(f"RESPONSE: {json.dumps(response, ensure_ascii=False)}")
                        break
                    elif response["type"] == "stream_chunk":
                        print(f"STREAM_CHUNK: {json.dumps(response, ensure_ascii=False)}")
                    elif response["type"] == "stream_end":
                        break
                    elif response["type"] == "error":
                        print(f"ERROR: {json.dumps(response, ensure_ascii=False)}")
                        break
                        
            except json.JSONDecodeError:
                print(f"ERROR: Invalid JSON command")
            except Exception as e:
                print(f"ERROR: {e}")
                
    except KeyboardInterrupt:
        pass
    finally:
        # 清理
        request_queue.put(None)
        process.join(timeout=10)
        if process.is_alive():
            process.terminate()

if __name__ == "__main__":
    main()
