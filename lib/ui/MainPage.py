from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from lib.utils.FontUtils import getFontSTXName


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="首页：题目列表",font_name = getFontSTXName()))

        btn = Button(text="去解题页面",font_name = getFontSTXName())
        btn.bind(on_press=self.go_to_coding)
        layout.add_widget(btn)

        self.add_widget(layout)

    def go_to_coding(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "coding"