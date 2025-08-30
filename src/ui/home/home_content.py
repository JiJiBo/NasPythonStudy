import flet as ft
from typing import Callable, Optional

from flet.core.list_tile import ListTile

from src.ui.study.study_pagel import study_page


class HomeContent(ft.Column):
    """
    具有生命周期的首页内容组件
    """

    def __init__(self, on_button_click: Optional[Callable] = None, on_back=None):
        super().__init__()
        self.on_button_click_callback = on_button_click or self.default_button_click
        self._is_mounted = False
        self.on_back = on_back

        # 初始化组件
        self._build_ui()

    def _build_ui(self):
        """构建UI组件"""
        self.controls = [
            ListTile(
                leading=ft.Icon(ft.Icons.HISTORY, size=30),
                title=ft.Text("第一节", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("数据结构", size=12, color=ft.Colors.GREY),
                on_click=lambda e: study_page(self.page, on_back=self.on_back),
            )
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

    def did_mount(self):
        """组件挂载到页面时调用"""
        self._is_mounted = True

    def will_unmount(self):
        """组件从页面卸载时调用"""
        self._is_mounted = False

    def default_button_click(self, e):
        """默认按钮点击处理"""
        # 显示点击反馈
        button = e.control
        original_bgcolor = button.bgcolor

        # 动画效果
        button.bgcolor = ft.Colors.GREEN_100
        self.update()

        # 添加临时提示
        import threading
        def reset_button():
            if self._is_mounted:
                button.bgcolor = original_bgcolor
                self.update()

        timer = threading.Timer(0.3, reset_button)
        timer.daemon = True
        timer.start()
