from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from lib.utils.FontUtils import getFontSTXName


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Header
        header = Label(
            text="题目列表",
            font_name=getFontSTXName(),
            font_size=30,
            size_hint=(1, 0.2),
            color=get_color_from_hex("#2c3e50")
        )
        layout.add_widget(header)

        # Problem list
        problems = [
            "1. 两数之和",
            "2. 两数相加",
            "3. 无重复字符的最长子串",
            "4. 寻找两个正序数组的中位数",
            "5. 最长回文子串"
        ]

        for problem in problems:
            btn = Button(
                text=problem,
                font_name=getFontSTXName(),
                background_color=get_color_from_hex("#3498db"),
                color=(1, 1, 1, 1),
                size_hint=(1, 0.12)
            )
            btn.bind(on_press=lambda instance, p=problem: self.show_problem_detail(p))
            layout.add_widget(btn)

        # Navigation button
        nav_btn = Button(
            text="去解题页面",
            font_name=getFontSTXName(),
            background_color=get_color_from_hex("#e74c3c"),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15)
        )
        nav_btn.bind(on_press=self.go_to_coding)
        layout.add_widget(nav_btn)

        self.add_widget(layout)

    def show_problem_detail(self, problem):
        print(f"Selected problem: {problem}")
        # In a real app, you would navigate to a problem detail screen

    def go_to_coding(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "coding"
