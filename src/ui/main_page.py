import flet as ft

from src.str.APP_CONFIG import APP_NAME


def main_page(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 页面切换函数
    def change_page(e):
        index = page.navigation_bar.selected_index
        content_area.content = pages[index]
        page.update()

    # 创建导航栏
    page.navigation_bar = ft.NavigationBar(
        on_change=change_page,
        bgcolor=ft.Colors.GREEN_50,
        indicator_color=ft.Colors.GREEN_400,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        elevation=10,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="主页",
                selected_icon=ft.Icons.HOME_OUTLINED
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NEAR_ME,
                label="我的",
                selected_icon=ft.Icons.NEAR_ME_OUTLINED
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS,
                label="设置",
                selected_icon=ft.Icons.SETTINGS_OUTLINED
            ),
        ]
    )

    # 主页内容
    home_content = ft.Column(
        controls=[
            ft.Icon(ft.Icons.HOME, size=50, color=ft.Colors.GREEN_700),
            ft.Text("欢迎使用我的应用", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("这是主页内容区域", size=16, color=ft.Colors.GREY_600),
            ft.ElevatedButton(
                "了解更多",
                icon=ft.Icons.INFO,
                on_click=lambda e: print("主页按钮点击")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # 我的页面内容
    my_content = ft.Column(
        controls=[
            ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.BLUE_700),
            ft.Text("个人中心", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("这里可以查看和管理您的个人信息", size=16, color=ft.Colors.GREY_600),
            ft.Row(
                [
                    ft.CircleAvatar(
                        foreground_image_src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1480&q=80",
                        content=ft.Text("用户"),
                        max_radius=40,
                    ),
                    ft.Column(
                        [
                            ft.Text("张三", weight=ft.FontWeight.BOLD),
                            ft.Text("zhangsan@example.com"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # 设置页面内容
    settings_content = ft.Column(
        controls=[
            ft.Icon(ft.Icons.SETTINGS, size=50, color=ft.Colors.ORANGE_700),
            ft.Text("设置", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("在这里配置您的应用偏好", size=16, color=ft.Colors.GREY_600),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Switch(label="夜间模式", value=False),
                        ft.Switch(label="消息通知", value=True),
                        ft.Switch(label="自动更新", value=True),
                    ],
                    spacing=10,
                ),
                padding=20,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # 所有页面列表
    pages = [home_content, my_content, settings_content]

    # 内容区域
    content_area = ft.Container(
        content=pages[0],  # 默认显示主页
        alignment=ft.alignment.center,
        expand=True
    )

    # 添加内容到页面
    page.add(content_area)

    page.update()

