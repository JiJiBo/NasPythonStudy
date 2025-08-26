from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from lib.utils.FontUtils import getFontSTX


# 第一个页面
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="首页：题目列表"))

        btn = Button(text="去解题页面")
        btn.bind(on_press=self.go_to_coding)
        layout.add_widget(btn)

        self.add_widget(layout)

    def go_to_coding(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "coding"

# 第二个页面
class CodingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="解题页面：输入代码"))
        btn_back = Button(text="返回首页")
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home"

class MyApp(App):
    def build(self):
        LabelBase.register(
            name="Chinese",
            fn_regular=getFontSTX()
        )
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CodingScreen(name="coding"))
        return sm

if __name__ == "__main__":
    MyApp().run()
