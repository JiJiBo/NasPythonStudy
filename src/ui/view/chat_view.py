import flet as ft
from src.utils.ChatUtils import AIRequestHandler


class ChatContent(ft.Column):
    def __init__(self, **kwargs):
        self.ai_handler = AIRequestHandler()

        # 聊天显示区用 ListView
        self.chat_area = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

        self.input_box = ft.TextField(
            hint_text="请输入内容...",
            expand=True,
            multiline=True,
            height=100,
            on_submit=self.send_message
        )
        self.send_button = ft.IconButton(ft.Icons.SEND, on_click=self.send_message)

        input_row = ft.Row([self.input_box, self.send_button], alignment=ft.MainAxisAlignment.CENTER)

        super().__init__(
            controls=[self.chat_area, input_row],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def add_message(self, text, is_user=False):
        color = ft.Colors.BLUE if is_user else ft.Colors.GREEN
        # 使用 Markdown 控件显示 Markdown 格式的文本，并支持文本选择和复制
        self.chat_area.controls.append(
            ft.Container(
                content=ft.Markdown(text, selectable=True),
                padding=10,
                bgcolor=color.with_opacity(0.1, color),
                border_radius=8
            )
        )
        self.update()

    def send_message(self, e):
        user_text = self.input_box.value.strip()
        self.send_custom_message(user_text)

    def send_custom_message(self, user_text):
        if not user_text:
            return
        self.add_message(user_text, is_user=True)
        self.input_box.value = ""
        self.update()

        # 新建 AI 消息容器
        self._ai_container = ft.Container(
            content=ft.Markdown("", selectable=True),
            padding=10,
            bgcolor=ft.Colors.GREEN.with_opacity(0.1, ft.Colors.GREEN),
            border_radius=8
        )
        self.chat_area.controls.append(self._ai_container)
        self.update()

        # 流式更新 AI 回复
        def callback(chunk):
            self._ai_container.content.value += chunk
            self.update()

        def error_callback(err):
            self.add_message(f"错误: {err}", is_user=False)

        self.ai_handler.stream_response(user_text, callback, error_callback)
