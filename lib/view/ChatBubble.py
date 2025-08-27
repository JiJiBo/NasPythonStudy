import threading
import requests
import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget

from lib.utils.ChatUtils import AIRequestHandler
from lib.utils.FontUtils import getFontSTXName

Window.clearcolor = (1, 1, 1, 1)


class ChatBubble(BoxLayout):
    def __init__(self, text="", is_ai=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(5), dp(5)]
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(80)
        self.is_ai = is_ai

        alignment = 'left' if is_ai else 'right'

        self.main_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            padding=[dp(15), dp(10)]
        )

        if not is_ai:
            self.main_container.add_widget(Widget(size_hint=(1, 1)))

        self.answer_label = Label(
            text=text,
            text_size=(Window.width * 0.6, None),
            size_hint=(None, None),
            halign='left',
            valign='middle',
            font_name=getFontSTXName(),
            color=(0, 0, 0, 1)
        )
        self.answer_label.bind(texture_size=self.update_answer_size)

        self.answer_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
        )
        self.answer_container.add_widget(self.answer_label)

        with self.answer_container.canvas.before:
            if is_ai:
                Color(0.6, 0.9, 0.6, 1)
            else:
                Color(0.3, 0.6, 1, 1)
            self.rect = RoundedRectangle(
                pos=self.answer_container.pos,
                size=self.answer_container.size,
                radius=[dp(15)]
            )
        self.answer_container.bind(pos=self.update_rect, size=self.update_rect)

        self.main_container.add_widget(self.answer_container)

        if is_ai:
            self.main_container.add_widget(Widget(size_hint=(1, 1)))

        self.add_widget(self.main_container)

        # 缓冲区优化
        self._buffer = ""
        self._update_ev = None

    def update_answer_size(self, instance, value):
        instance.size = value
        self.answer_container.size = (value[0] + dp(30), value[1] + dp(20))
        self.main_container.height = self.answer_container.height
        self.height = self.main_container.height

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def append_text(self, new_text):
        self._buffer += new_text
        if not self._update_ev:
            self._update_ev = Clock.schedule_once(self.flush_text, 0.05)

    def flush_text(self, dt):
        if self._buffer:
            self.answer_label.text += self._buffer
            self._buffer = ""
            self.answer_label.texture_update()
            self.update_answer_size(self.answer_label, self.answer_label.texture_size)
        self._update_ev = None


class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

        self.ai_handler = AIRequestHandler()

        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll.add_widget(self.chat_layout)
        self.add_widget(self.scroll)

        input_layout = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        self.input_box = TextInput(
            multiline=False,
            hint_text="输入消息...",
            size_hint=(0.8, 1),
            font_name=getFontSTXName(),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(10), dp(10)]
        )
        self.send_button = Button(
            text='发送',
            size_hint=(0.2, 1),
            font_name=getFontSTXName(),
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.send_button.bind(on_release=self.send_message)
        input_layout.add_widget(self.input_box)
        input_layout.add_widget(self.send_button)
        self.add_widget(input_layout)

        self.input_box.bind(on_text_validate=self.send_message)

    def send_message(self, instance=None):
        user_text = self.input_box.text.strip()
        if not user_text:
            return

        user_bubble = ChatBubble(user_text, is_ai=False)
        self.chat_layout.add_widget(user_bubble)
        self.input_box.text = ''

        self.scroll_to_bottom()

        threading.Thread(target=self.ai_reply_stream, args=(user_text,), daemon=True).start()

    def ai_reply_stream(self, user_text):
        ai_bubble = None
        event = threading.Event()

        def create_ai_bubble(dt):
            nonlocal ai_bubble
            ai_bubble = ChatBubble("", is_ai=True)
            self.chat_layout.add_widget(ai_bubble)
            self.scroll_to_bottom()
            event.set()

        Clock.schedule_once(create_ai_bubble, 0)
        event.wait()

        def handle_response(text):
            Clock.schedule_once(lambda dt, t=text: ai_bubble.append_text(t), 0)

        def handle_error(error_msg):
            error_text = f"\n\n错误: {error_msg}"
            Clock.schedule_once(lambda dt, t=error_text: ai_bubble.append_text(t), 0)

        try:
            self.ai_handler.stream_response(
                prompt=user_text,
                callback=handle_response,
                error_callback=handle_error
            )
        finally:
            Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.2)

    def scroll_to_bottom(self):
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

