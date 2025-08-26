from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

from lib.ui.MainPage import MainScreen
from lib.ui.SplashPage import SplashScreen
from lib.utils.FontUtils import getFontSTX, getFontSTXName
from test.TestPage import TestScreen


class MyApp(App):
    def build(self):
        LabelBase.register(
            name=getFontSTXName(),
            fn_regular=getFontSTX()
        )
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(TestScreen(name="test"))
        return sm

if __name__ == "__main__":
    MyApp().title = "编程学习App"
    MyApp().run()
