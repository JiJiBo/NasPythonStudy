from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

from lib.ui.MainPage import SplashScreen
from lib.utils.FontUtils import getFontSTX, getFontSTXName



class MyApp(App):
    def build(self):
        LabelBase.register(
            name=getFontSTXName(),
            fn_regular=getFontSTX()
        )
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        return sm

if __name__ == "__main__":
    MyApp().run()
