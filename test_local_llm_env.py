#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试LocalLLMEngine是否能正确使用python_env中的torch
"""

import sys
from pathlib import Path

# 添加python_env到Python路径
python_env_path = Path("python_env")
if python_env_path.exists():
    sys.path.insert(0, str(python_env_path))
    print(f"✅ 已添加python_env到Python路径: {python_env_path}")

# 测试torch导入
try:
    import torch
    print(f"✅ torch导入成功")
    print(f"torch版本: {torch.__version__}")
    print(f"torch路径: {torch.__file__}")
    print(f"CUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA版本: {torch.version.cuda}")
        print(f"GPU数量: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
except ImportError as e:
    print(f"❌ torch导入失败: {e}")

# 测试transformers导入
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print(f"✅ transformers导入成功")
    print(f"transformers版本: {transformers.__version__}")
except ImportError as e:
    print(f"❌ transformers导入失败: {e}")

# 测试LocalLLMEngine
try:
    from src.utils.LocalLLMEngine import local_llm_engine
    print(f"✅ LocalLLMEngine导入成功")
    print(f"设备: {local_llm_engine.device}")
    
    # 获取模型信息
    model_info = local_llm_engine.get_model_info()
    print(f"模型信息: {model_info}")
    
except ImportError as e:
    print(f"❌ LocalLLMEngine导入失败: {e}")
except Exception as e:
    print(f"❌ LocalLLMEngine测试失败: {e}")

print("\n=== 测试完成 ===")
