# 本地LLM模型集成说明

## 功能概述

本项目已集成本地LLM模型支持，允许用户下载和使用Hugging Face上的小型语言模型，无需依赖外部API服务。

## 支持的模型

### 1. Qwen2.5-0.5B-Instruct
- **大小**: 约1GB
- **语言**: 中文优化
- **特点**: 轻量级中文对话模型，适合中文场景
- **推荐用途**: 中文问答、对话、文本生成

### 2. TinyLlama-1.1B-Chat
- **大小**: 约2GB  
- **语言**: 英文优化
- **特点**: 超轻量级英文对话模型
- **推荐用途**: 英文问答、代码生成、文本处理

## 安装依赖

### 自动安装
```bash
python install_dependencies.py
```

### 手动安装
```bash
# 基础依赖
pip install requests tqdm

# 本地模型推理依赖
pip install torch transformers

# UI依赖（如果使用图形界面）
pip install flet
```

## 使用方法

### 1. 通过设置界面使用

1. 启动应用
2. 进入"LLM模型设置"页面
3. 选择"本地模型"作为模型类型
4. 选择要使用的模型（Qwen2.5-0.5B 或 TinyLlama-1.1B）
5. 点击"下载模型"按钮下载模型文件
6. **支持断点续传**: 如果下载过程中退出应用，再次进入时会自动检测并恢复下载进度
7. 下载完成后，点击"保存配置"
8. 返回聊天界面即可使用本地模型

### 2. 通过代码使用

```python
from src.utils.ChatUtils import AIRequestHandlerWithHistory

# 创建聊天处理器
chat_handler = AIRequestHandlerWithHistory()

# 设置本地模型配置
from src.db.llm_config_db import LLMConfigDB
db = LLMConfigDB()
config_id = db.save_config(
    provider="local_model",
    model="qwen2.5-0.5b",
    base_url=None,
    api_key=None
)
db.set_current_config(config_id)

# 刷新配置
chat_handler.refresh_config()

# 发送消息
chat_id = "test_chat"
response = chat_handler.get_single_response(chat_id, "你好，请介绍一下自己")
print(response)
```

## 文件结构

```
assets/
└── models/                    # 模型文件存储目录
    ├── qwen2.5-0.5b/         # Qwen2.5-0.5B模型文件
    │   ├── config.json
    │   ├── model.safetensors
    │   ├── tokenizer.json
    │   └── ...
    └── tinyllama-1.1b/       # TinyLlama-1.1B模型文件
        ├── config.json
        ├── model.safetensors
        ├── tokenizer.json
        └── ...

src/utils/
├── ModelManager.py           # 模型下载和管理
├── LocalLLMEngine.py        # 本地模型推理引擎
└── ChatUtils.py             # 聊天工具（已更新支持本地模型）

src/ui/llm/
└── llm_settings.py          # LLM设置界面（已更新支持本地模型）
```

## 技术实现

### 模型管理器 (ModelManager)
- 负责从Hugging Face下载模型文件
- 管理模型存储和状态检查
- 支持进度回调和错误处理

### 本地LLM引擎 (LocalLLMEngine)
- 使用transformers库加载和运行模型
- 支持单次响应和流式响应
- 自动设备检测（CPU/GPU）
- 内存管理和模型卸载

### 聊天工具集成 (ChatUtils)
- 无缝集成本地模型到现有聊天系统
- 支持历史记录和上下文管理
- 统一的API接口

## 性能优化建议

### 1. 硬件要求
- **最低配置**: 4GB RAM, 2GB 可用磁盘空间
- **推荐配置**: 8GB RAM, 4GB 可用磁盘空间
- **GPU支持**: 支持CUDA的GPU可显著提升推理速度

### 2. 内存管理
- 模型会在首次使用时加载到内存
- 使用完毕后可调用 `local_llm_engine.unload_model()` 释放内存
- 应用重启时会自动卸载模型

### 3. 模型选择
- 中文场景推荐使用 Qwen2.5-0.5B
- 英文场景推荐使用 TinyLlama-1.1B
- 根据设备性能选择合适的模型大小

## 故障排除

### 1. 模型下载失败
- **网络连接问题**: 应用已集成国内镜像支持，会自动切换到 `https://hf-mirror.com` 等镜像源
- **连接重置错误**: 如果遇到 "ConnectionResetError" 或 "远程主机强迫关闭连接"，系统会自动重试并切换镜像
- **重试机制**: 每个文件最多重试3次，每次重试间隔2秒
- **磁盘空间**: 确保有足够的磁盘空间（至少2GB）
- **手动重试**: 如果自动重试失败，可以手动点击"重新下载"按钮

### 2. 下载中断恢复
- **自动检测**: 应用启动时会自动检测未完成的下载
- **断点续传**: 支持从中断点继续下载，不会重新下载已完成的文件
- **状态显示**: 界面会显示"恢复下载"按钮和当前下载进度
- **手动恢复**: 如果自动恢复失败，可以手动点击"恢复下载"按钮
- **状态文件**: 下载状态保存在 `download_state.json` 文件中

### 3. 模型加载失败
- 检查transformers库是否正确安装
- 确保模型文件完整下载
- 检查系统内存是否充足

### 4. 推理速度慢
- 考虑使用GPU加速
- 减少输入长度
- 选择更小的模型

## 扩展功能

### 添加新模型
1. 在 `ModelManager.py` 的 `supported_models` 中添加新模型配置
2. 在 `llm_settings.py` 的模型下拉框中添加选项
3. 测试新模型的下载和推理功能

### 自定义模型路径
可以通过修改 `ModelManager` 的 `assets_dir` 参数来指定自定义的模型存储路径。

## 注意事项

1. **首次使用**: 需要下载模型文件，可能需要较长时间
2. **存储空间**: 确保有足够的磁盘空间存储模型文件
3. **网络要求**: 下载模型需要稳定的网络连接
4. **隐私保护**: 本地模型不会发送数据到外部服务器
5. **性能权衡**: 本地模型响应速度可能比云端API慢，但提供更好的隐私保护

## 更新日志

- **v1.3**: 添加下载进度恢复功能，支持断点续传
  - 实现下载状态持久化，支持应用重启后恢复下载
  - 添加智能断点续传，跳过已下载的文件
  - 实时显示下载进度和状态信息
  - 支持下载中断后自动恢复
  - 优化用户体验，无需重新开始下载

- **v1.2**: 添加国内镜像支持，解决网络连接问题
  - 集成国内镜像源 `https://hf-mirror.com`
  - 添加自动重试机制（最多3次重试）
  - 改进网络错误处理和连接重置错误处理
  - 添加镜像状态显示和切换功能
  - 优化下载进度显示和用户反馈

- **v1.1**: 修复模型下载404错误，优化用户体验
  - 修复了special_tokens_map.json等可选文件下载失败的问题
  - 移除了"local"选项，只保留"local_model"选项
  - 全面中文化界面和提示信息
  - 优化了下载进度显示和错误处理

- **v1.0**: 初始版本，支持Qwen2.5-0.5B和TinyLlama-1.1B模型
  - 集成模型下载和管理功能
  - 支持单次和流式响应
  - 完整的UI集成
