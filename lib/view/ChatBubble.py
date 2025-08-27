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

from lib.utils.FontUtils import getFontSTXName

# 假设的字体工具函数，如果没有请替换为实际字体


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

        # 对齐方式取决于是否是AI
        alignment = 'left' if is_ai else 'right'

        # 主容器
        self.main_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            padding=[dp(15), dp(10)]
        )

        # 根据对齐方式设置容器内子元素的排列
        if not is_ai:
            self.main_container.add_widget(Widget(size_hint=(1, 1)))  # 占位空间

        # 回答标签
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

        # 回答容器
        self.answer_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
        )
        self.answer_container.add_widget(self.answer_label)

        with self.answer_container.canvas.before:
            if is_ai:
                Color(0.6, 0.9, 0.6, 1)  # AI消息背景色
            else:
                Color(0.3, 0.6, 1, 1)  # 用户消息背景色
            self.rect = RoundedRectangle(
                pos=self.answer_container.pos,
                size=self.answer_container.size,
                radius=[dp(15)]
            )
        self.answer_container.bind(pos=self.update_rect, size=self.update_rect)

        self.main_container.add_widget(self.answer_container)

        if is_ai:
            self.main_container.add_widget(Widget(size_hint=(1, 1)))  # 占位空间

        self.add_widget(self.main_container)

        # 思考中动画区
        self.thinking_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(20)
        )

        if not is_ai:
            self.thinking_container.add_widget(Widget(size_hint=(1, 1)))  # 占位空间

        self.thinking_label = Label(
            text="",
            font_size="12sp",
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(None, None),
            halign="left",
            valign="middle",
            opacity=0
        )
        self.thinking_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'size', value)
        )

        thinking_inner_container = BoxLayout(size_hint=(None, None))
        thinking_inner_container.add_widget(self.thinking_label)
        self.thinking_container.add_widget(thinking_inner_container)

        if is_ai:
            self.thinking_container.add_widget(Widget(size_hint=(1, 1)))  # 占位空间

        self.add_widget(self.thinking_container)
        self._thinking_ev = None

    def start_thinking(self):
        """开始显示 ... 动画"""
        self.thinking_label.opacity = 1

        def animate(dt):
            dots = self.thinking_label.text.count(".")
            if dots >= 3:
                self.thinking_label.text = ""
            else:
                self.thinking_label.text += "."

        self._thinking_ev = Clock.schedule_interval(animate, 0.5)

    def stop_thinking(self):
        """停止动画并清空"""
        if self._thinking_ev:
            self._thinking_ev.cancel()
            self._thinking_ev = None
        self.thinking_label.text = ""
        self.thinking_label.opacity = 0

    def update_answer_size(self, instance, value):
        instance.size = value
        self.answer_container.size = (value[0] + dp(30), value[1] + dp(20))
        self.main_container.height = self.answer_container.height
        self.height = self.main_container.height + self.thinking_container.height
        self.parent.parent.parent.scroll_to_bottom()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def append_text(self, new_text, is_think=False):
        if is_think:
            if not self._thinking_ev:
                self.start_thinking()
        else:
            self.stop_thinking()
            self.answer_label.text += new_text
            self.answer_label.texture_update()
            self.update_answer_size(self.answer_label, self.answer_label.texture_size)


class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

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

        # 绑定回车键发送消息
        self.input_box.bind(on_text_validate=self.send_message)

    def send_message(self, instance=None):
        user_text = self.input_box.text.strip()
        if not user_text:
            return

        # 添加用户消息
        user_bubble = ChatBubble(user_text, is_ai=False)
        self.chat_layout.add_widget(user_bubble)
        self.input_box.text = ''

        # 滚动到底部
        self.scroll_to_bottom()

        # 开线程调用流式 AI 回复
        threading.Thread(target=self.ai_reply_stream, args=(user_text,), daemon=True).start()

    def ai_reply_stream(self, user_text):
        # 创建AI消息气泡
        ai_bubble = None

        def create_ai_bubble(dt):
            nonlocal ai_bubble
            ai_bubble = ChatBubble("", is_ai=True)
            self.chat_layout.add_widget(ai_bubble)
            self.scroll_to_bottom()

        # 在主线程中创建气泡
        Clock.schedule_once(create_ai_bubble, 0)

        # 等待气泡创建完成
        import time
        time.sleep(0.1)

        # DeepSeek API调用
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "deepseek-r1:14b",
            "prompt": user_text,
            "stream": True
        }

        try:
            with requests.post(url, json=payload, stream=True) as res:
                for line in res.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        response_text = chunk.get("response", "")

                        if response_text:
                            # 在主线程中更新UI
                            Clock.schedule_once(
                                lambda dt, text=response_text: ai_bubble.append_text(text, is_think=False),
                                0
                            )
        except Exception as e:
            error_msg = f"\n\n错误: {str(e)}"
            Clock.schedule_once(
                lambda dt, text=error_msg: ai_bubble.append_text(text, is_think=False),
                0
            )

    def scroll_to_bottom(self):
        # 确保布局更新后再滚动
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)
