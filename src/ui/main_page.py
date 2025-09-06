import flet as ft

from src.str.APP_CONFIG import APP_NAME
from src.ui.home.home_content import HomeContent
from src.ui.home.mine_content import MineContent
from src.ui.home.setting_content import SettingContent
from src.ui.llm.llm_settings import llm_setting_page
from src.ui.view.chat_view import ChatPullToRefresh


def main_page(page: ft.Page, selected_index: int = 0):
    page.clean()
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT

    # 页面切换函数
    def change_page(e):
        index = page.navigation_bar.selected_index

        # 在切换页面前，清理当前页面的异步操作
        try:
            current_content = content_area.content
            if hasattr(current_content, 'will_unmount'):
                current_content.will_unmount()
        except Exception as ex:
            print(f"清理页面时出错: {ex}")

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
            ft.NavigationBarDestination(
                icon=ft.Icons.CHAT,
                label="Chat",
                selected_icon=ft.Icons.CHAT_OUTLINED
            ),
        ]
    )

    home_content = HomeContent(on_back=lambda a, selected_index=0: main_page(page, selected_index=selected_index))
    my_content = MineContent()
    settings_content = SettingContent(
        page,
        on_back=lambda a, selected_index=0: main_page(page, selected_index=selected_index)
    )
    chat_content = ChatPullToRefresh(chat_id="comment")
    # 所有页面列表
    pages = [home_content, my_content, settings_content, chat_content]

    # 设置默认选中的底部标签
    try:
        page.navigation_bar.selected_index = selected_index
    except Exception:
        page.navigation_bar.selected_index = 0

    # 内容区域
    content_area = ft.Container(
        content=pages[page.navigation_bar.selected_index],
        expand=True
    )

    # 添加内容到页面
    page.add(content_area)
    page.update()
