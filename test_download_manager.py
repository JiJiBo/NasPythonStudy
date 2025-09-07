"""
测试新的下载管理器
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.DownloadManager import download_manager
import time

def test_download_manager():
    """测试下载管理器"""
    print("=== 测试下载管理器 ===")
    
    # 测试事件订阅
    def on_status_changed(data):
        model_name = data["model_name"]
        status = data["status"]
        print(f"📡 事件: {model_name} - {status['status']} - {status['progress']:.1f}%")
    
    # 订阅事件
    download_manager.subscribe_download_events(on_status_changed)
    
    # 检查未完成的下载
    print("\n=== 检查未完成的下载 ===")
    all_statuses = download_manager.get_all_download_statuses()
    for model_name, status in all_statuses.items():
        print(f"📁 {model_name}: {status.status} - {status.progress:.1f}%")
    
    # 测试下载状态
    print("\n=== 测试下载状态 ===")
    test_model = "qwen2.5-coder-1.5b-q4_k_m"
    status = download_manager.get_download_status(test_model)
    if status:
        print(f"📊 {test_model} 状态: {status.status}")
        print(f"   进度: {status.progress:.1f}%")
        print(f"   大小: {status.downloaded_size}/{status.total_size}")
    else:
        print(f"📊 {test_model} 无下载状态")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_download_manager()
