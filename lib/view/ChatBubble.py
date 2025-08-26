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

Window.clearcolor = (1, 1, 1, 1)  # 整体白色背景


class ChatBubble(BoxLayout):
    def __init__(self, text, is_ai=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = [dp(5), dp(5)]
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(50)  # Initial height, will be updated

        # Create container for the bubble
        container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            padding=[dp(15), dp(10)]
        )

        # Create the label
        label = Label(
            text=text,
            text_size=(Window.width * 0.6, None),
            size_hint=(None, None),
            halign='left',
            valign='middle',
            font_name = getFontSTXName(),
            color=(0, 0, 0, 1)  # Black text for better contrast
        )
        label.bind(texture_size=self.update_label_size)

        # Add label to container
        container.add_widget(label)

        # Set initial container size
        container.size = (label.width + dp(30), label.height + dp(20))

        # Draw rounded rectangle background
        with container.canvas.before:
            if is_ai:
                Color(0.6, 0.9, 0.6, 1)  # AI绿色
            else:
                Color(0.3, 0.6, 1, 1)  # 用户蓝色
            self.rect = RoundedRectangle(
                pos=container.pos,
                size=container.size,
                radius=[dp(15)]
            )

        # Update rectangle when container moves/resizes
        container.bind(pos=self.update_rect, size=self.update_rect)

        # Add appropriate spacing based on sender
        if is_ai:
            self.add_widget(container)
            self.add_widget(Widget())  # Spacer
        else:
            self.add_widget(Widget())  # Spacer
            self.add_widget(container)

    def update_label_size(self, instance, value):
        instance.size = value
        instance.parent.size = (value[0] + dp(30), value[1] + dp(20))
        self.height = value[1] + dp(30)  # Update bubble height

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

        # 聊天区域
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(5), dp(5)]
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll.add_widget(self.chat_layout)
        self.add_widget(self.scroll)

        # 输入区域
        input_layout = BoxLayout(
            size_hint=(1, 0.15),
            spacing=dp(10),
            padding=[dp(5), dp(5)]
        )
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

    def send_message(self, instance):
        user_text = self.input_box.text.strip()
        if not user_text:
            return
        self.chat_layout.add_widget(ChatBubble(user_text, is_ai=False))
        self.input_box.text = ''
        Clock.schedule_once(lambda dt: self.ai_reply(user_text), 0.5)
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.6)

    def ai_reply(self, user_text):
        ai_text = f"AI 回复: {user_text[::-1]}"
        self.chat_layout.add_widget(ChatBubble(ai_text, is_ai=True))
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)

    def scroll_to_bottom(self):
        if self.chat_layout.children:
            self.scroll.scroll_to(self.chat_layout.children[0])