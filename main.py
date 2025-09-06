import flet as ft

from src.ui.splash_page import splash_page


def main(page: ft.Page):
    page.window_icon = "icon.png"
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 800
    page.window_min_height = 600
    page.theme = ft.Theme(font_family="Microsoft YaHei")  # 或者 "Microsoft YaHei", "Noto Sans", "PingFang SC"
    page.bgcolor = ft.Colors.WHITE
    splash_page(page)


ft.app(main)
