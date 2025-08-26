from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

from lib.utils.FontUtils import getFontSTXName


class ChatBubble(BoxLayout):
    def __init__(self, text, is_ai=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 10

        label = Label(
            text=text,
            size_hint=(None, None),
            text_size=(250, None),
            halign='left',
            valign='middle',
            padding=(10,10),
            font_name = getFontSTXName()
        )
        label.bind(texture_size=label.setter('size'))

        if is_ai:
            self.add_widget(label)
            self.add_widget(BoxLayout())  # 占位，让气泡靠左
        else:
            self.add_widget(BoxLayout())  # 占位，让气泡靠右
            self.add_widget(label)

class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # 聊天区域
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll.add_widget(self.chat_layout)
        self.add_widget(self.scroll)

        # 输入区域
        input_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.input_box = TextInput(multiline=False)
        self.send_button = Button(text='发送', size_hint=(0.2, 1),font_name=getFontSTXName())
        self.send_button.bind(on_release=self.send_message)
        input_layout.add_widget(self.input_box)
        input_layout.add_widget(self.send_button)
        self.add_widget(input_layout)

    def send_message(self, instance):
        user_text = self.input_box.text.strip()
        if not user_text:
            return
        # 显示用户消息
        self.chat_layout.add_widget(ChatBubble(user_text, is_ai=False))
        self.input_box.text = ''
        # 模拟 AI 回复
        Clock.schedule_once(lambda dt: self.ai_reply(user_text), 0.5)
        # 滚动到底部
        Clock.schedule_once(lambda dt: self.scroll.scroll_to(self.chat_layout.children[0]), 0.6)

    def ai_reply(self, user_text):
        # 这里可以替换成真实 AI 接口调用
        ai_text = f"AI 回复: {user_text[::-1]}"  # 示例：把用户文字倒过来
        self.chat_layout.add_widget(ChatBubble(ai_text, is_ai=True))
        Clock.schedule_once(lambda dt: self.scroll.scroll_to(self.chat_layout.children[0]), 0.1)