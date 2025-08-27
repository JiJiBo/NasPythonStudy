import flet as ft

from src.str.APP_CONFIG import APP_NAME


def main_page(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 创建导航栏 - 修改了颜色
    page.navigation_bar = ft.NavigationBar(
        bgcolor=ft.Colors.GREEN_50,  # 浅绿色背景
        indicator_color=ft.Colors.GREEN_400,  # 指示器颜色
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        elevation=10,  # 添加阴影效果
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="主页",
                selected_icon=ft.Icons.HOME_OUTLINED
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.MY_LOCATION,
                label="我的",
                selected_icon=ft.Icons.MY_LOCATION_OUTLINED
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS,
                label="设置",
                selected_icon=ft.Icons.SETTINGS_OUTLINED
            ),
        ]
    )

    # 创建主要内容区域
    content = ft.Column(
        controls=[
            ft.Icon(ft.Icons.COLOR_LENS, size=50, color=ft.Colors.BLUE_700),
            ft.Text("欢迎使用我的应用", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("导航栏颜色已修改为蓝色主题", size=16, color=ft.Colors.GREY_600),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # 添加内容到页面
    page.add(
        ft.Container(
            content=content,
            alignment=ft.alignment.center,
            expand=True
        )
    )

    page.update()

