#!/usr/bin/env python3
"""
测试增量更新系统
"""

import flet as ft
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.UpdateManager import update_manager
from src.utils.UpdateBuilder import UpdateBuilder

def test_update_builder():
    """测试UpdateBuilder"""
    print("=== 测试UpdateBuilder ===")
    
    # 创建构建器
    builder = UpdateBuilder("./src", "./test_updates")
    
    # 生成更新信息
    update_info = builder.generate_update_json(
        version="0.1.1",
        changelog="新增一键更新功能",
        previous_version="0.1.0"
    )
    
    print(f"生成更新信息: {len(update_info['files'])} 个文件")
    print(f"总大小: {update_info['total_size']} 字节")
    
    # 保存更新信息
    json_path = builder.save_update_json(update_info)
    print(f"更新信息已保存到: {json_path}")
    
    return True

def test_update_manager():
    """测试UpdateManager"""
    print("\n=== 测试UpdateManager ===")
    
    # 配置更新管理器
    update_manager.update_config.update({
        "version_url": "file://./version.json",  # 使用本地文件测试
        "current_version": "0.1.0"
    })
    
    # 获取本地版本信息
    local_info = update_manager.get_local_version_info()
    print(f"本地版本信息: {local_info}")
    
    # 检查更新（这里会失败，因为没有真实的更新源）
    try:
        app_update = update_manager.check_app_update()
        print(f"应用更新检查: {app_update}")
    except Exception as e:
        print(f"应用更新检查失败（预期）: {e}")
    
    return True

def test_update_ui():
    """测试更新UI"""
    print("\n=== 测试更新UI ===")
    
    def main(page: ft.Page):
        page.title = "更新系统测试"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 800
        page.window_height = 600
        
        # 创建测试按钮
        test_btn = ft.ElevatedButton(
            "测试更新功能",
            on_click=lambda e: show_update_dialog(page)
        )
        
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("增量更新系统测试", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    test_btn,
                    ft.Text("点击按钮测试更新功能", size=14, color=ft.Colors.GREY)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                alignment=ft.alignment.center
            )
        )
    
    def show_update_dialog(page):
        """显示更新对话框"""
        # 创建状态显示
        status_text = ft.Text("正在检查更新...", size=14, color=ft.Colors.BLUE)
        progress_bar = ft.ProgressBar(width=400, visible=False)
        
        # 创建检查按钮
        check_btn = ft.ElevatedButton(
            "检查更新",
            icon=ft.Icons.REFRESH,
            on_click=lambda e: check_updates(status_text, progress_bar, check_btn)
        )
        
        # 创建对话框
        dialog = ft.AlertDialog(
            title=ft.Text("一键更新测试"),
            content=ft.Container(
                content=ft.Column([
                    status_text,
                    progress_bar,
                    ft.Divider(),
                    check_btn
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=500,
                height=300
            ),
            actions=[
                ft.TextButton("关闭", on_click=lambda e: page.close(dialog))
            ]
        )
        
        page.dialog = dialog
        page.open(dialog)
        page.update()
        
        # 自动检查更新
        check_updates(status_text, progress_bar, check_btn)
    
    def check_updates(status_text, progress_bar, check_btn):
        """检查更新"""
        import threading
        
        def check_thread():
            try:
                # 模拟检查过程
                status_text.value = "正在检查应用更新..."
                status_text.update()
                
                import time
                time.sleep(1)
                
                status_text.value = "正在检查模型更新..."
                status_text.update()
                time.sleep(1)
                
                # 模拟发现更新
                status_text.value = "发现可用更新！"
                status_text.color = ft.Colors.ORANGE
                status_text.update()
                
                # 添加更新按钮
                update_btn = ft.ElevatedButton(
                    "模拟更新",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: simulate_update(status_text, progress_bar)
                )
                
                # 这里需要更新对话框内容，但为了简化，我们只更新状态
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
        import threading
        
        def update_thread():
            try:
                progress_bar.visible = True
                progress_bar.update()
                
                for i in range(101):
                    status_text.value = f"下载更新: {i}%"
                    progress_bar.value = i / 100
                    progress_bar.update()
                    status_text.update()
                    
                    import time
                    time.sleep(0.05)
                
                status_text.value = "更新完成！"
                status_text.color = ft.Colors.GREEN
                status_text.update()
                
            except Exception as e:
                status_text.value = f"更新失败: {str(e)}"
                status_text.color = ft.Colors.RED
                status_text.update()
        
        thread = threading.Thread(target=update_thread, daemon=True)
        thread.start()
    
    # 运行Flet应用
    ft.app(target=main)

def main():
    """主函数"""
    print("🚀 开始测试增量更新系统...")
    
    try:
        # 测试UpdateBuilder
        test_update_builder()
        
        # 测试UpdateManager
        test_update_manager()
        
        print("\n✅ 所有测试完成！")
        print("\n📱 启动UI测试...")
        
        # 启动UI测试
        test_update_ui()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
