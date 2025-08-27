import flet as ft

from src.ui.splash_page import splash_page


def main(page: ft.Page):
    page.bgcolor = ft.Colors.WHITE
    splash_page(page)


ft.app(main)
