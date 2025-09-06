# Python环境集成

这个文件夹包含了Python环境集成的相关脚本和配置文件。

## 文件说明

### 核心脚本

- `python_launcher.py` - Python环境启动器，提供Python环境管理功能
- `install_cuda_torch.py` - CUDA版本torch安装脚本
- `check_environment.py` - 环境检查脚本
- `requirements.txt` - 依赖包列表

### 使用方法

#### 1. 检查环境状态
```bash
python python_env/check_environment.py
```

#### 2. 安装CUDA版本torch
```bash
python python_env/install_cuda_torch.py
```

#### 3. 在代码中使用
```python
from python_env.python_launcher import get_python_executable, install_package

# 获取Python可执行文件路径
python_exe = get_python_executable()

# 安装包
install_package("torch", "https://download.pytorch.org/whl/cu121")
```

## 功能特性

### Python环境管理器
- 自动检测Python可执行文件
- 支持包安装、卸载、版本检查
- 环境信息获取
- 跨平台支持（Windows/Linux/macOS）

### CUDA支持
- 自动检测CUDA版本
- 根据CUDA版本选择对应的torch版本
- 支持CUDA 11.8, 12.0, 12.1等版本
- 自动验证GPU可用性

### 环境检查
- 系统信息检查
- CUDA信息检查
- PyTorch状态检查
- 依赖包检查

## 支持的CUDA版本

| CUDA版本 | PyTorch索引URL | 说明 |
|---------|---------------|------|
| 12.8+ | cu121 | 使用CUDA 12.1兼容版本 |
| 12.7 | cu121 | 使用CUDA 12.1兼容版本 |
| 12.6 | cu121 | 使用CUDA 12.1兼容版本 |
| 12.1 | cu121 | 使用CUDA 12.1版本 |
| 12.0 | cu120 | 使用CUDA 12.0版本 |
| 11.8 | cu118 | 使用CUDA 11.8版本 |

## 故障排除

### 常见问题

1. **CUDA不可用**
   - 检查NVIDIA驱动是否正确安装
   - 运行 `nvidia-smi` 确认GPU状态
   - 重新安装CUDA版本的torch

2. **包安装失败**
   - 检查网络连接
   - 尝试使用不同的索引URL
   - 检查Python环境是否正确

3. **编码问题**
   - 确保系统支持UTF-8编码
   - 在Windows上可能需要设置环境变量

### 调试命令

```bash
# 检查Python版本
python --version

# 检查已安装的包
pip list

# 检查torch状态
python -c "import torch; print(torch.cuda.is_available())"

# 检查CUDA版本
nvidia-smi
```

## 更新日志

- v1.0.0 - 初始版本，支持基本的Python环境管理
- v1.1.0 - 添加CUDA版本torch安装支持
- v1.2.0 - 添加环境检查功能
