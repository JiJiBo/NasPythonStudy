#!/usr/bin/env python3
"""
简单的下载按钮测试应用
用于验证下载按钮是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import flet as ft
from src.utils.LocalModelManager import local_model_manager

def main(page: ft.Page):
    page.title = "下载按钮测试"
    page.window_width = 600
    page.window_height = 400
    
    # 创建测试按钮
    test_button = ft.ElevatedButton("测试下载按钮", on_click=test_download_click)
    
    # 创建状态显示
    status_text = ft.Text("点击按钮测试下载功能", size=16)
    
    def test_download_click(e):
        print("下载按钮被点击!")
        status_text.value = "下载按钮被点击了!"
        page.update()
        
        # 显示下载对话框
        show_download_dialog()
    
    def show_download_dialog():
        available_models = local_model_manager.get_available_models()
        installed_models = local_model_manager.get_installed_models()
        installed_names = [m.name for m in installed_models]
        
        # 创建可下载的模型列表
        download_options = []
        for model_name, model_info in available_models.items():
            if model_name not in installed_names:
                size_mb = model_info.size // (1024 * 1024)
                display_name = model_name.replace("qwen2.5-coder-1.5b-", "Qwen-")
                text = f"{display_name} ({size_mb}MB)"
                
                download_options.append(
                    ft.dropdown.Option(
                        key=model_name,
                        text=text
                    )
                )
        
        if not download_options:
            status_text.value = "所有模型都已安装"
            page.update()
            return
        
        download_dropdown = ft.Dropdown(
            options=download_options,
            width=400
        )
        
        def confirm_download(e):
            if download_dropdown.value:
                print(f"确认下载模型: {download_dropdown.value}")
                status_text.value = f"开始下载: {download_dropdown.value}"
                page.close(dlg)
                page.update()
            else:
                print("没有选择模型")
        
        def cancel_download(e):
            print("取消下载")
            page.close(dlg)
        
        dlg = ft.AlertDialog(
            title=ft.Text("下载模型"),
            content=ft.Column([
                ft.Text("选择要下载的模型:", size=14),
                download_dropdown
            ], spacing=10),
            actions=[
                ft.ElevatedButton("下载", on_click=confirm_download),
                ft.TextButton("取消", on_click=cancel_download)
            ]
        )
        
        print("打开下载对话框")
        page.dialog = dlg
        page.open(dlg)
        page.update()
    
    # 添加控件到页面
    page.add(
        ft.Column([
            ft.Text("下载按钮测试应用", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            test_button,
            ft.Divider(),
            status_text
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
