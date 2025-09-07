#!/usr/bin/env python3
"""
演示一键更新功能
"""

import flet as ft
import sys
import os
import threading
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main(page: ft.Page):
    page.title = "AI辅助Python学习 - 一键更新演示"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 900
    page.window_height = 700
    page.padding = 20
    
    # 创建状态显示
    status_text = ft.Text("准备就绪", size=16, color=ft.Colors.BLUE)
    progress_bar = ft.ProgressBar(width=600, visible=False)
    
    # 创建更新按钮
    check_update_btn = ft.ElevatedButton(
        "检查更新",
        icon=ft.Icons.REFRESH,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        ),
        on_click=lambda e: check_updates(status_text, progress_bar, check_update_btn)
    )
    
    # 创建模拟更新按钮
    simulate_update_btn = ft.ElevatedButton(
        "模拟更新",
        icon=ft.Icons.DOWNLOAD,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE
        ),
        on_click=lambda e: simulate_update(status_text, progress_bar)
    )
    
    # 创建功能说明
    feature_list = ft.Column([
        ft.Text("🚀 一键更新功能特性", size=20, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("✅ 自动检查应用和模型更新", size=14),
        ft.Text("✅ 支持增量更新，节省带宽", size=14),
        ft.Text("✅ 断点续传，网络中断可恢复", size=14),
        ft.Text("✅ 多镜像源，提高下载速度", size=14),
        ft.Text("✅ 自动备份，更新失败可恢复", size=14),
        ft.Text("✅ 文件完整性验证", size=14),
        ft.Text("✅ 实时进度显示", size=14),
        ft.Text("✅ 一键批量更新", size=14),
    ], spacing=8)
    
    # 创建使用说明
    usage_guide = ft.Column([
        ft.Text("📖 使用方法", size=18, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("1. 在设置页面点击'一键更新'", size=14),
        ft.Text("2. 系统自动检查可用更新", size=14),
        ft.Text("3. 选择要更新的内容", size=14),
        ft.Text("4. 点击更新按钮开始下载", size=14),
        ft.Text("5. 等待更新完成", size=14),
    ], spacing=6)
    
    # 创建主界面
    page.add(
        ft.Container(
            content=ft.Column([
                # 标题
                ft.Text("AI辅助Python学习应用", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("一键更新功能演示", size=18, color=ft.Colors.GREY, text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                
                # 状态显示区域
                ft.Container(
                    content=ft.Column([
                        ft.Text("更新状态", size=16, weight=ft.FontWeight.BOLD),
                        status_text,
                        progress_bar
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10
                ),
                
                # 按钮区域
                ft.Row([
                    check_update_btn,
                    simulate_update_btn
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                
                ft.Divider(),
                
                # 功能说明和使用指南
                ft.Row([
                    feature_list,
                    ft.VerticalDivider(),
                    usage_guide
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND, expand=True)
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            padding=20
        )
    )

def check_updates(status_text, progress_bar, check_btn):
    """检查更新"""
    def check_thread():
        try:
            # 更新状态
            def update_status(text, color=ft.Colors.BLUE):
                status_text.value = text
                status_text.color = color
                status_text.update()
            
            # 模拟检查过程
            update_status("正在检查应用更新...", ft.Colors.BLUE)
            time.sleep(1)
            
            update_status("正在检查模型更新...", ft.Colors.BLUE)
            time.sleep(1)
            
            # 模拟发现更新
            update_status("发现可用更新！", ft.Colors.ORANGE)
            
            # 更新按钮文本
            check_btn.text = "重新检查"
            check_btn.update()
            
        except Exception as e:
            status_text.value = f"检查更新失败: {str(e)}"
            status_text.color = ft.Colors.RED
            status_text.update()
    
    thread = threading.Thread(target=check_thread, daemon=True)
    thread.start()

def simulate_update(status_text, progress_bar):
    """模拟更新过程"""
    def update_thread():
        try:
            progress_bar.visible = True
            progress_bar.update()
            
            # 模拟下载过程
            for i in range(101):
                if i < 30:
                    status_text.value = f"下载应用更新: {i}%"
                elif i < 70:
                    status_text.value = f"下载模型文件: {i}%"
                else:
                    status_text.value = f"安装更新: {i}%"
                
                progress_bar.value = i / 100
                progress_bar.update()
                status_text.update()
                
                time.sleep(0.03)  # 加快演示速度
            
            # 完成
            status_text.value = "更新完成！请重启应用"
            status_text.color = ft.Colors.GREEN
            status_text.update()
            
            # 隐藏进度条
            progress_bar.visible = False
            progress_bar.update()
            
        except Exception as e:
            status_text.value = f"更新失败: {str(e)}"
            status_text.color = ft.Colors.RED
            status_text.update()
    
    thread = threading.Thread(target=update_thread, daemon=True)
    thread.start()

if __name__ == "__main__":
    print("🚀 启动一键更新功能演示...")
    print("📱 演示内容:")
    print("   - 检查更新流程")
    print("   - 模拟下载过程")
    print("   - 进度显示效果")
    print("   - 功能特性介绍")
    print("\n💡 提示: 这是演示版本，实际功能已集成到主应用中")
    
    ft.app(target=main)
