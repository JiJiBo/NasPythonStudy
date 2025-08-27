import flet as ft
from flet.core.types import FontWeight

from src.str.APP_CONFIG import APP_NAME


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
