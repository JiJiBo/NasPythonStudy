import flet as ft

from src.str.APP_CONFIG import APP_NAME


def main_page(page: ft.Page):
    page.clean()
    page.title = APP_NAME
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="主页"),
            ft.NavigationBarDestination(icon=ft.Icons.MY_LOCATION, label="我的"),
        ]
    )
    page.navigation_bar.bg_color = ft.Colors.GREEN_50
    page.add(ft.Text("Body!"))
    page.update()
