import flet as ft
import threading

from src.str.APP_CONFIG import APP_NAME, auto_load_local_model
from src.ui.home.home_content import HomeContent
from src.ui.home.mine_content import MineContent
from src.ui.home.setting_content import SettingContent
from src.ui.llm.llm_settings import llm_setting_page
from src.ui.view.chat_view import ChatPullToRefresh


def main_page(page: ft.Page, selected_index: int = 0):
    page.clean()
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 在后台线程中自动加载本地模型
    def auto_load_model():
        try:
            print("🚀 开始自动加载本地模型...")
            success = auto_load_local_model()
            if success:
                print("✅ 本地模型自动加载完成")
                # 可以在这里添加成功提示
            else:
                print("ℹ️ 没有需要自动加载的本地模型")
        except Exception as e:
            print(f"❌ 自动加载模型时出错: {e}")
    
    # 启动自动加载线程
    threading.Thread(target=auto_load_model, daemon=True).start()

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
