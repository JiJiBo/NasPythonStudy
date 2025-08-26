from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

from lib.utils.FontUtils import getFontSTXName
from lib.utils.ImgUtils import getImgPath


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=30)

        # Add app logo
        logo = Image(source=getImgPath("logo.png"), size_hint=(0.5, 0.5))
        # Note: For this example, I'm using a placeholder image source
        # In a real app, you would use your own logo.png file

        # If you don't have a logo.png, you can replace with a label:
        # logo = Label(text="[Your App Logo]", font_size=50, markup=True)
        layout.add_widget(logo)

        # Add loading text
        loading_text = Label(
            text="Loading...",
            font_name=getFontSTXName(),
            font_size=20,
            color=get_color_from_hex("#3498db")
        )
        layout.add_widget(loading_text)

        self.add_widget(layout)

    def on_enter(self):
        # Schedule transition to main page after 1 second
        Clock.schedule_once(self.go_to_main, 10)

    def go_to_main(self, dt):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "main"