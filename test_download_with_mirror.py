#!/usr/bin/env python3
"""
测试使用镜像源下载
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.LocalModelManager import local_model_manager

def test_download_with_mirror():
    print("测试使用镜像源下载...")
    
    # 获取可用模型
    available_models = local_model_manager.get_available_models()
    
    # 选择一个未安装的模型进行测试
    for name, info in available_models.items():
        if not local_model_manager.is_model_installed(name):
            print(f"\n开始测试下载模型: {name}")
            print(f"文件大小: {info.size // (1024*1024)}MB")
            
            def progress_callback(name, progress, downloaded, total):
                if progress % 10 == 0:  # 每10%显示一次
                    print(f"下载进度: {progress:.1f}% ({downloaded//1024//1024}MB/{total//1024//1024}MB)")
            
            def error_callback(error):
                print(f"下载错误: {error}")
            
            def success_callback():
                print(f"✅ 下载成功: {name}")
            
            # 开始下载
            success = local_model_manager.download_model(name, progress_callback, error_callback, success_callback)
            print(f"下载启动结果: {success}")
            
            if success:
                print("下载已开始，请等待完成...")
                print("注意：这是一个大文件，可能需要几分钟时间")
            break
    else:
        print("所有模型都已安装")

if __name__ == "__main__":
    test_download_with_mirror()
