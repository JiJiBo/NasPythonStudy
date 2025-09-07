#!/usr/bin/env python3
"""
调试LLM设置页面的按钮问题
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
    page.title = "LLM设置调试"
    page.window_width = 800
    page.window_height = 600
    
    # 创建状态显示
    status_text = ft.Text("准备测试", size=16)
    
    # 创建本地模型下拉框
    local_model_dropdown = ft.Dropdown(
        label="选择本地模型",
        width=400,
        options=[]
    )
    
    # 创建按钮
    download_btn = ft.ElevatedButton("下载模型")
    load_btn = ft.ElevatedButton("加载模型")
    
    # 刷新模型列表
    def refresh_models():
        available_models = local_model_manager.get_available_models()
        installed_models = local_model_manager.get_installed_models()
        
        local_model_dropdown.options.clear()
        
        for model_name, model_info in available_models.items():
            is_installed = any(m.name == model_name for m in installed_models)
            status = "✓" if is_installed else "✗"
            size_mb = model_info.size // (1024 * 1024)
            
            display_name = model_name.replace("qwen2.5-coder-1.5b-", "Qwen-")
            text = f"{display_name} ({size_mb}MB) {status}"
            
            local_model_dropdown.options.append(
                ft.dropdown.Option(
                    key=model_name,
                    text=text,
                    disabled=not is_installed
                )
            )
        
        page.update()
    
    # 按钮事件处理
    def on_download_click(e):
        print("下载按钮被点击!")
        status_text.value = "下载按钮被点击!"
        page.update()
        
        # 显示下载对话框
        show_download_dialog()
    
    def on_load_click(e):
        print("加载按钮被点击!")
        if local_model_dropdown.value:
            status_text.value = f"加载模型: {local_model_dropdown.value}"
        else:
            status_text.value = "请先选择模型"
        page.update()
    
    def show_download_dialog():
        available_models = local_model_manager.get_available_models()
        installed_models = local_model_manager.get_installed_models()
        installed_names = [m.name for m in installed_models]
        
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
                print(f"确认下载: {download_dropdown.value}")
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
    
    # 绑定按钮事件
    download_btn.on_click = on_download_click
    load_btn.on_click = on_load_click
    
    # 初始化
    refresh_models()
    
    # 添加控件到页面
    page.add(
        ft.Column([
            ft.Text("LLM设置调试", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            local_model_dropdown,
            ft.Row([download_btn, load_btn], spacing=10),
            ft.Divider(),
            status_text
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
