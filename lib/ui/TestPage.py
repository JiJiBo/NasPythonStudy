from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from lib.utils.FontUtils import getFontSTXName
from lib.view.ChatBubble import ChatBubble, ChatScreen


class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chat_bubble = ChatScreen( )

        self.add_widget(chat_bubble)

    def go_to_coding(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "coding"
