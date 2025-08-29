import flet as ft
from src.ui.llm.llm_settings import llm_setting_page


class SettingContent(ft.Column):
    """
    具有生命周期的首页内容组件
    """

    def __init__(self, page: ft.Page, on_back=None):
        super().__init__()
        self.p = page
        self.on_back = on_back
        # 初始化组件
        self._build_ui()

    def _build_ui(self):
        """构建UI组件"""
        self.controls = [
            ft.ListTile(
                ft.Text("大模型设置"),
                on_click=lambda e: llm_setting_page(self.p, on_back=self.on_back),
            )

        ]
        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

    def did_mount(self):
        pass

    def will_unmount(self):
        pass
