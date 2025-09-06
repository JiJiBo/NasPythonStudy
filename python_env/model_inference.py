#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的模型推理脚本
用于避免DLL冲突，在python_env环境中运行
"""

import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path

# 设置标准输出编码为UTF-8
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# 全局变量存储模型和tokenizer
_global_tokenizer = None
_global_model = None
_global_model_path = None
_global_device = None

def load_model(model_path, device="cuda"):
    """加载模型和tokenizer（只加载一次）"""
    global _global_tokenizer, _global_model, _global_model_path, _global_device
    
    # 如果已经加载了相同的模型，直接返回
    if (_global_tokenizer is not None and _global_model is not None and 
        _global_model_path == model_path and _global_device == device):
        return _global_tokenizer, _global_model
    
    try:
        # 加载tokenizer
        _global_tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        
        # 加载模型
        _global_model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        
        if device == "cpu":
            _global_model = _global_model.to("cpu")
        
        _global_model_path = model_path
        _global_device = device
        
        return _global_tokenizer, _global_model
        
    except Exception as e:
        print(f"MODEL_LOAD_ERROR: {e}")
        return None, None

def format_qwen_messages(messages):
    """格式化Qwen模型的消息"""
    formatted_text = ""
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        if role == "user":
            formatted_text += f"<|im_start|>user\n{content}<|im_end|>\n"
        elif role == "assistant":
            formatted_text += f"<|im_start|>assistant\n{content}<|im_end|>\n"
    
    # 添加assistant开始标记
    formatted_text += "<|im_start|>assistant\n"
    return formatted_text

def format_simple_messages(messages):
    """格式化简单消息"""
    formatted_text = ""
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        if role == "user":
            formatted_text += f"用户: {content}\n"
        elif role == "assistant":
            formatted_text += f"助手: {content}\n"
    
    formatted_text += "助手: "
    return formatted_text

def generate_response(tokenizer, model, messages, device, max_length=2048, temperature=0.7):
    """生成响应"""
    try:
        # 构建对话格式
        if any("qwen" in str(messages).lower() for msg in messages):
            text = format_qwen_messages(messages)
        else:
            text = format_simple_messages(messages)
        
        # 编码输入
        tokenized = tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=2048,
            padding=False
        )
        inputs = tokenized["input_ids"].to(device)
        attention_mask = tokenized["attention_mask"].to(device)
        
        # 生成响应
        with torch.no_grad():
            input_length = inputs.shape[1]
            # 确保max_new_tokens有足够的长度，避免输出过短
            max_new_tokens = max(200, min(max_length - input_length, 1024))
            
            # 调试信息
            print(f"DEBUG: input_length={input_length}, max_length={max_length}, max_new_tokens={max_new_tokens}", file=sys.stderr)
            
            # 使用流式生成
            from transformers import TextIteratorStreamer
            import threading
            
            # 创建流式输出器
            streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
            
            # 在单独线程中生成
            generation_kwargs = {
                "input_ids": inputs,
                "attention_mask": attention_mask,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "do_sample": True,
                "pad_token_id": tokenizer.eos_token_id,
                "eos_token_id": tokenizer.eos_token_id,
                "repetition_penalty": 1.1,
                "streamer": streamer
            }
            
            thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
            thread.start()
            
            # 流式输出响应
            response = ""
            for new_text in streamer:
                response += new_text
                print(f"STREAM_CHUNK: {new_text}", flush=True)
            
            thread.join()
        
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
        
        # 再次清理空白字符
        response = response.strip()
        
        print(f"RESPONSE_SUCCESS: {response}")
        return response
        
    except Exception as e:
        print(f"RESPONSE_ERROR: {e}")
        return f"生成响应时出错: {e}"

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python model_inference.py <command> [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        if len(sys.argv) < 4:
            print("用法: python model_inference.py generate <model_path> <messages_json> [max_length] [temperature] [device]")
            sys.exit(1)
        
        model_path = sys.argv[2]
        messages_json = sys.argv[3]
        max_length = int(sys.argv[4]) if len(sys.argv) > 4 else 512
        temperature = float(sys.argv[5]) if len(sys.argv) > 5 else 0.7
        device = sys.argv[6] if len(sys.argv) > 6 else "cuda"
        
        try:
            messages = json.loads(messages_json)
            
            # 加载模型
            tokenizer, model = load_model(model_path, device)
            if tokenizer is None or model is None:
                print("RESPONSE_ERROR: 模型加载失败")
                sys.exit(1)
            
            # 生成响应
            response = generate_response(tokenizer, model, messages, device, max_length, temperature)
            # generate_response函数已经打印了RESPONSE_SUCCESS，这里不需要再打印
            
        except Exception as e:
            print(f"RESPONSE_ERROR: {e}")
            sys.exit(1)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
