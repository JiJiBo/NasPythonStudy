import flet as ft
from flet.core.animation import AnimationCurve

from src.ui.view.RitchView import RichContent
from src.utils.ChatUtils import AIRequestHandler, ai_handler


class ChatContent(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll_count = 0
        # 聊天显示区
        self.chat_area = ft.ListView(
            expand=True,
            spacing=5,
            padding=10,
            auto_scroll=True,
        )

        self.input_box = ft.TextField(
            hint_text="请输入内容...",
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=5,
            on_submit=self.send_message
        )
        self.send_button = ft.IconButton(ft.Icons.SEND, on_click=self.send_message)

        input_row = ft.Row([self.input_box, self.send_button], alignment=ft.MainAxisAlignment.CENTER)

        # 快速到底部按钮，初始隐藏
        self.scroll_bottom_button = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            on_click=self._scroll_to_bottom,
            bgcolor=ft.Colors.GREEN,
            visible=True,
            mini=True,
        )

        # 组合页面
        super().__init__(
            controls=[self.chat_area, self.scroll_bottom_button, input_row],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
        self.expand = True

        # 自动滚动标志
        self.auto_scroll = True
        self.chat_area.on_scroll = self.on_list_scroll

    def on_list_scroll(self, e):
        # 计算距离底部的距离
        distance_from_bottom = e.max_scroll_extent - e.pixels
        if distance_from_bottom > 200:
            # 距离底部较远，显示按钮，禁止自动滚动
            self.auto_scroll = False
            self.scroll_bottom_button.visible = True
        else:
            # 接近底部，自动滚动
            self.auto_scroll = True
            self.scroll_bottom_button.visible = False

        self.scroll_bottom_button.update()

    def scroll_to_bottom(self, e=None):

        if self.scroll_count % 20 != 0:
            self.scroll_count += 1
            return
        self.scroll_count += 1
        self._scroll_to_bottom()

    def _scroll_to_bottom(self, e=None):
        # 滚动到底部
        self.chat_area.scroll_to(offset=0)
        self.auto_scroll = True
        self.scroll_bottom_button.visible = False
        self.scroll_bottom_button.update()

    def add_message(self, text, is_user=False):
        color = ft.Colors.BLUE if is_user else ft.Colors.GREEN
        container = ft.Container(
            content=RichContent(text),
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border_radius=8,
            margin=ft.margin.only(bottom=5)
        )
        self.chat_area.controls.append(container)
        self.update()

        # 如果处于自动滚动状态，滚动到底部
        if self.auto_scroll:
            self.scroll_to_bottom()

    def send_message(self, e):
        user_text = self.input_box.value.strip()
        self.send_custom_message(user_text)

    def send_custom_message(self, user_text):
        if not user_text:
            return
        self.add_message(user_text, is_user=True)
        self.input_box.value = ""
        self.input_box.focus()
        self.update()

        # AI 回复容器
        self._ai_container = ft.Container(
            content=RichContent(""),
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
            border_radius=8,
            margin=ft.margin.only(bottom=5)
        )
        self.chat_area.controls.append(self._ai_container)
        self.update()

        # 流式更新 AI 回复
        def callback(chunk):
            self._ai_container.content.parse_and_add_content(chunk)
            self.update()
            if self.auto_scroll:
                self.scroll_to_bottom()

            self.update()

        def error_callback(err):
            self.add_message(f"错误: {err}", is_user=False)

        ai_handler.stream_response(user_text, callback, error_callback)
