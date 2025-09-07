#!/usr/bin/env python3
"""
简单的按钮测试
"""

import flet as ft

def main(page: ft.Page):
    page.title = "按钮测试"
    page.window_width = 400
    page.window_height = 300
    
    # 创建状态显示
    status_text = ft.Text("点击按钮测试", size=16)
    
    def on_button_click(e):
        print("按钮被点击了!")
        status_text.value = "按钮被点击了! 时间: " + str(ft.datetime.now())
        page.update()
    
    # 创建按钮
    test_button = ft.ElevatedButton("测试按钮", on_click=on_button_click)
    
    # 添加控件到页面
    page.add(
        ft.Column([
            ft.Text("按钮测试应用", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            test_button,
            ft.Divider(),
            status_text
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
