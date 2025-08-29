import threading
import platform
import time
from typing import Optional

import flet as ft

from src.str.APP_CONFIG import ai_handler, kvUtils
from src.ui.view.PullToRefresh import PullToRefreshList
from src.ui.view.RitchView import RichContent


class ChatPullToRefresh(PullToRefreshList):
    def __init__(self, chat_id=None, **kwargs):
        super().__init__(**kwargs)
        self.chat_id = chat_id
        self.history_offset_id = None

        max_load_history = kvUtils.get_int("max_load_history", default=20)
        self.history_limit = max_load_history
        # 底部输入
        self.input_box = ft.TextField(
            hint_text="请输入内容...",
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=5,
            on_submit=self.send_message,
        )
        # 方法定义
        # 绑定焦点事件
        self.input_box.on_focus = self._on_focus
        self.input_box.on_blur = self._on_blur
        self.input_box.on_key_down = self.key_down_handler  # 绑定键盘事件

        self.send_button = ft.IconButton(ft.Icons.SEND, on_click=self.send_message)
        self.input_row = ft.Row([self.input_box, self.send_button], alignment=ft.MainAxisAlignment.CENTER)
        self.controls.append(self.input_row)

    def key_down_handler(self, e: ft.KeyboardEvent):
        # 检查是否按下回车且没有按 Shift
        if e.key == "Enter" and not e.shift:
            self.send_message(None)  # 注意 send_message 有一个参数 e
            e.prevent_default = True  # 阻止默认换行

    # ------------------ 下拉刷新 ------------------
    def refresh_data(self):
        if not self.chat_id:
            return
        messages = []  # 示例
        if messages:
            self.list_view.controls.clear()
            for msg in messages:
                self.add_message(msg["text"], is_user=msg.get("is_user", False))
            self.history_offset_id = messages[0].get("id")
            self.scroll_to_bottom()
        self.refresh_indicator.visible = False
        self.refreshing = False
        self.update()

    # ------------------ 消息操作 ------------------
    def add_message(self, text, is_user=False):
        color = ft.Colors.BLUE if is_user else ft.Colors.GREEN
        container = ft.Container(
            content=RichContent(text),
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border_radius=8,
            margin=ft.margin.only(bottom=5)
        )
        self.list_view.controls.append(container)
        self.update()
        if self.auto_scroll:
            self.scroll_to_bottom()

    def send_message(self, e):
        user_text = self.input_box.value.strip()
        if not user_text:
            return
        self.add_message(user_text, is_user=True)
        self.input_box.value = ""
        self.input_box.focus()
        self.update()
        # AI 回复
        self._ai_container = ft.Container(
            content=RichContent(""),
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
            border_radius=8,
            margin=ft.margin.only(bottom=5)
        )
        self.list_view.controls.append(self._ai_container)
        self.update()

        def callback(chunk):
            self._ai_container.content.parse_and_add_content(chunk)
            self.update()
            if self.auto_scroll:
                self.scroll_to_bottom()

        def error_callback(err):
            self.add_message(f"错误: {err}", is_user=False)

        ai_handler.send_message(self.chat_id, user_text, callback, error_callback, n=self.history_limit)

    # ------------------ 历史消息 ------------------
    def load_recent_history_after_mount(self):
        if not self.chat_id:
            return
        messages = ai_handler.get_recent_history(self.chat_id, last_id=None, limit=self.history_limit)
        for msg in messages:
            self.add_message(msg[2], is_user=(msg[1] == "user"))
        if messages:
            self.history_offset_id = messages[0][0]

    def did_mount(self):
        self.load_recent_history_after_mount()
        self.input_focused = False
        self.scroll_to_bottom()
        self.start_keyboard_listener()

    def _on_focus(self, e):
        self.input_focused = True

    def _on_blur(self, e):
        self.input_focused = False

    def start_keyboard_listener(self):
        system = platform.system().lower()

        def listen_keyboard():
            if system == "darwin":  # macOS 用 pynput
                from pynput import keyboard as pk

                def on_press(key):
                    if not self.input_focused:
                        return
                    try:
                        if key == pk.Key.enter:
                            self.send_message(None)
                    except Exception as e:
                        print("键盘监听错误:", e)

                with pk.Listener(on_press=on_press) as listener:
                    listener.join()
            else:  # Windows/Linux 用 keyboard
                import keyboard
                enter_pressed = False
                while not self.stop_listener:
                    if self.input_focused:
                        if keyboard.is_pressed("enter") and not keyboard.is_pressed("shift"):
                            if not enter_pressed:
                                self.send_message(None)
                                enter_pressed = True
                        else:
                            enter_pressed = False
                    time.sleep(0.05)

        self.stop_listener = False
        self.listener_thread = threading.Thread(target=listen_keyboard, daemon=True)
        self.listener_thread.start()

    def stop_keyboard_listener(self):
        self.stop_listener = True
        if hasattr(self, "listener_thread") and self.listener_thread:
            self.listener_thread.join(timeout=0.1)

    def will_unmount(self):
        self.stop_keyboard_listener()
