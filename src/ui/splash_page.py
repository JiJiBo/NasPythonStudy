import threading
import time

import flet as ft
from flet.core.types import FontWeight

from src.str.APP_CONFIG import APP_NAME
from src.ui.main_page import main_page


def splash_page(page: ft.Page):
    page.clean()
    page.add(
        ft.Container(

            ft.Column(
                [
                    ft.Image("icon.png", width=256, height=256),
                    ft.Text(APP_NAME, color="black", size=40, weight=FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # 垂直居中
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 水平居中
            ),
            bgcolor=ft.Colors.WHITE,
            width=page.width,
            height=page.height,
            alignment=ft.alignment.center,
        )
    )
    def go_to_main():
        time.sleep(1)  # Wait for 1 second
        page.clean()
        main_page(page)
        page.update()
    threading.Thread(target=go_to_main, daemon=True).start()