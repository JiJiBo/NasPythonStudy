import os

import flet as ft
import yaml
from docutils.nodes import container
from flet.core.markdown import MarkdownCodeTheme

from src.ui.view.CodeRunner import CodeRunner
from src.ui.view.chat_view import ChatPullToRefresh


def study_page(study_dir, page: ft.Page, on_back=None):
    previous_navigation_bar = getattr(page, "navigation_bar", None)
    previous_appbar = getattr(page, "appbar", None)
    study_md = os.path.join(study_dir, "study.md")
    config_path = os.path.join(study_dir, "config.yaml")
    study_title = os.path.basename(study_dir)
    chat_id = study_dir
    with open(config_path, encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    print(config)
    isShowCode = config["code"]
    codeReturn = config["codeReturn"]
    codeExample = config["codeExample"]
    should = config["should"]
    if codeExample:
        code_path = os.path.join(study_dir, "code.py")
        with open(code_path, "r", encoding="utf-8") as f:
            codeBody = f.read()
        print("codeBody:", codeBody)
    previous_navigation_bar = getattr(page, "navigation_bar", None)
    if previous_navigation_bar is not None:
        page.navigation_bar = None
        page.update()

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
    if isShowCode:
        code_runner = CodeRunner(page, codeReturn)
        if codeExample:
            code_runner.set_default_code(codeBody)
    else:
        code_runner = ft.Container()
    # 右边聊天区
    chat_view = ChatPullToRefresh(chat_id=chat_id)
    chat_content = ft.Container(
        content=chat_view,
        alignment=ft.alignment.center,
        expand=True
    )

    def ask_ai(e):
        if should is not None:
            Q = f"你好，请帮我分析下代码，看看代码符合要求 {should} 吗？请给出中肯的评价 " + str(
                code_runner.get_run_result())
        else:
            Q = "你好，请帮我分析下代码，看看代码符合要求吗？请给出中肯的评价 " + str(code_runner.get_run_result())
        chat_view.ask(Q)

    if should is not None:
        # 左边学习区（md 渲染，可滚动，使用 ListView）
        ask_button = ft.Button(
            "AI的评价",
            on_click=ask_ai
        )
    else:
        ask_button = ft.Container()
    study_content = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Markdown(
                    md_content,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    code_theme=ft.MarkdownCodeTheme.GOOGLE_CODE,
                    on_tap_link=lambda e: page.launch_url(e.data),
                    expand=True,
                ),
                code_runner,
                ask_button
            ],
            expand=True,
            padding=10,
            spacing=10,
            auto_scroll=False,  # 不自动滚到底部
        ),
        width=700,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
    )

    page.add(ft.Row([study_content, chat_content], expand=True))
    page.update()
