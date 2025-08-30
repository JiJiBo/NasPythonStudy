import os

import flet as ft
from flet.core.markdown import MarkdownCodeTheme
from src.ui.view.chat_view import ChatPullToRefresh


def study_page(study_dir, page: ft.Page, on_back=None):
    previous_navigation_bar = getattr(page, "navigation_bar", None)
    previous_appbar = getattr(page, "appbar", None)
    study_md = os.path.join(study_dir, "study.md")
    study_title = os.path.basename(study_dir)
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
        title=ft.Text(study_title, size=20, weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.GREEN_50,
    )

    # 清理旧内容
    page.clean()

    # 读取 study.md 内容
    if os.path.exists(study_md):
        with open(study_md, "r", encoding="utf-8") as f:
            md_content = f.read()
    else:
        md_content = "# 没有找到 study.md 文件"

    # 左边学习区（md 渲染）
    study_content = ft.Container(
        content=ft.Markdown(
            md_content,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,  # 支持 GitHub 风格扩展
            code_theme=MarkdownCodeTheme.GOOGLE_CODE,
            on_tap_link=lambda e: page.launch_url(e.data),
            expand=True,
        ),
        width=700,
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
    )

    # 右边聊天区
    chat_content = ft.Container(
        content=ChatPullToRefresh(chat_id="comment"),
        alignment=ft.alignment.center,
        expand=True
    )

    page.add(ft.Row([study_content, chat_content], expand=True))
    page.update()
