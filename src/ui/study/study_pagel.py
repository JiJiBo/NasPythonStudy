import flet as ft
from flet.core.page import Window

from src.ui.view.chat_view import ChatPullToRefresh


def study_page(page: ft.Page, on_back=None):
    previous_navigation_bar = getattr(page, "navigation_bar", None)
    previous_appbar = getattr(page, "appbar", None)

    def back_click(e):
        if previous_navigation_bar is not None:
            page.navigation_bar = previous_navigation_bar
        page.appbar = previous_appbar

        if on_back:
            try:
                on_back(page, selected_index=0)
            except TypeError:
                on_back(page)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("返回主页"))
            page.snack_bar.open = True
        page.update()

    # 设置新 AppBar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=back_click),
        title=ft.Text("学习室", size=20, weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.GREEN_50,
    )

    # 清理旧内容
    page.clean()

    # 左边学习区（占固定宽度），右边聊天区（填满）
    study_content = ft.Container(ft.Text("学习内容区域"), width=700)
    chat_content = ft.Container(
        content=ChatPullToRefresh(chat_id="comment"),
        alignment=ft.alignment.center,
        expand=True
    )

    page.add(ft.Row([study_content, chat_content], expand=True))
    page.update()
