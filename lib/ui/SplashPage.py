from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

from assets.str.APP_CONFIG import APP_NAME
from lib.utils.FontUtils import getFontSTXName
from lib.utils.ImgUtils import getImgPath


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 设置白色背景
        with self.canvas.before:
            Color(1, 1, 1, 1)  # RGB白色，alpha=1
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # AnchorLayout 用于居中显示内容
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')

        # BoxLayout 用于垂直排列 logo 和文字
        layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(None, None))
        layout.width = 512
        layout.height = 512 + 50  # logo高度+文字高度大概50

        # Logo 图片
        logo = Image(
            source=getImgPath("logo.png"),
            size_hint=(None, None),
            size=(512, 512),
            allow_stretch=True
        )

        # 文本
        label = Label(
            text=APP_NAME,
            font_name=getFontSTXName(),
            font_size=36,
            color=get_color_from_hex("#2c3e50"),
            size_hint=(1, None),
            height=50
        )

        layout.add_widget(logo)
        layout.add_widget(label)
        anchor.add_widget(layout)
        self.add_widget(anchor)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        # 1秒后跳转到主页面
        Clock.schedule_once(self.go_to_main, 2)

    def go_to_main(self, dt):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "test"
