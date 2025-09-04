import os

import flet as ft
import yaml

from src.ui.view.CodeRunner import CodeRunner
from src.ui.view.chat_view import ChatPullToRefresh
from src.db.study_progress_db import StudyProgressDB


def study_page(study_dir, page: ft.Page, on_back=None):
    previous_navigation_bar = getattr(page, "navigation_bar", None)
    previous_appbar = getattr(page, "appbar", None)
    study_md = os.path.join(study_dir, "study.md")
    config_path = os.path.join(study_dir, "config.yaml")
    study_title = os.path.basename(study_dir)
    chat_id = study_dir
    
    # 初始化学习进度数据库
    db = StudyProgressDB("study_progress.db")
    
    # 提取章节和小节名称
    # 假设路径结构为: assets/study/第001章-开始/第001节-写在前面
    path_parts = study_dir.split(os.sep)
    chapter_name = None
    section_name = study_title  # 默认使用目录名作为小节名
    
    # 查找章节名（包含"章"的目录）
    for part in reversed(path_parts):
        if "章" in part:
            chapter_name = part
            break
    
    # 如果没有找到章节，尝试从父目录获取
    if not chapter_name:
        parent_dir = os.path.dirname(study_dir)
        if parent_dir:
            parent_name = os.path.basename(parent_dir)
            if "章" in parent_name:
                chapter_name = parent_name

    with open(config_path, encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
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
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK, 
            on_click=back_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.WHITE,
                color=ft.Colors.GREEN
            )
        ),
        title=ft.Text(study_title, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
        center_title=False,
        bgcolor=ft.Colors.WHITE,
        elevation=2,
        shadow_color=ft.Colors.BLACK26,
        surface_tint_color=ft.Colors.GREEN_50,
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
        code_alert = ft.Markdown(
            """
            # 请在此处输入代码
            """.strip(),
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            code_theme=ft.MarkdownCodeTheme.GOOGLE_CODE,
            on_tap_link=lambda e: page.launch_url(e.data),
            expand=True,
        )
        if codeExample:
            code_runner.set_default_code(codeBody)
    else:
        code_runner = ft.Container()
        code_alert = ft.Container()

    # 右边聊天区
    chat_view = ChatPullToRefresh(chat_id=chat_id)
    chat_content = ft.Container(
        content=chat_view,
        alignment=ft.alignment.center,
        expand=True,
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=12,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4)
        )
    )

    def ask_ai(e):
        if should is not None:
            Q = f"你好，请帮我分析下代码，看看代码符合要求 {should} 吗？请给出中肯的评价!只要符合要求，可执行，按要求输出，并且没有偷工减料，就可以，不用太严格。最后给出评分，只要按要求输出了，没有错误，就给100分满分。" + str(code_runner.get_run_result())
        else:
            Q = "你好，请帮我分析下代码，看看代码符合要求吗？请给出中肯的评价 " + str(code_runner.get_run_result())
        chat_view.ask(Q)

    def complete_study(e):
        """完成学习"""
        if not chapter_name:
            page.snack_bar = ft.SnackBar(
                ft.Text("无法确定章节信息，请检查路径结构", color=ft.Colors.RED)
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # 标记学习完成
        try:
            db.set_section_status(chapter_name, section_name, True)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"数据库更新失败: {ex}", color=ft.Colors.RED)
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # 关闭确认对话框
        if hasattr(page, 'dialog') and page.dialog:
            page.close(page.dialog)
        
        # 隐藏完成学习按钮
        complete_button.visible = False
        page.update()
        
        # 显示完成提示
        page.snack_bar = ft.SnackBar(
            ft.Text(f"🎉 恭喜！{section_name} 学习完成！", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN
        )
        page.snack_bar.open = True
        page.update()
        
        # 延迟1秒后退出页面
        def exit_page():
            import time
            time.sleep(1)
            back_click(None)
        
        import threading
        threading.Thread(target=exit_page, daemon=True).start()

    def show_completion_dialog(e):
        """显示完成确认对话框"""
        # 检查章节名是否存在
        if not chapter_name:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"无法确定章节信息！路径: {study_dir}", color=ft.Colors.RED)
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # 检查是否已经完成
        is_completed = db.is_section_completed(chapter_name, section_name)
        
        if is_completed:
            page.snack_bar = ft.SnackBar(
                ft.Text("该小节已经完成学习了！", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.BLUE
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # 创建确认对话框
        def close_dialog(e):
            page.close(confirm_dialog)
        
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("确认完成学习"),
            content=ft.Text(f"确定要标记「{section_name}」为已完成吗？\n\n完成后将无法撤销此操作。"),
            actions=[
                ft.TextButton("取消", on_click=close_dialog),
                ft.ElevatedButton(
                    "确认完成", 
                    on_click=complete_study,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = confirm_dialog
        page.open(confirm_dialog)
        page.update()

    if should is not None:
        ask_button = ft.Button("AI的评价", on_click=ask_ai)
        code_alert = ft.Markdown(
            f"""
            # 请在此处输入代码\n## 满足**{should}**的要求
            """.strip(),
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            code_theme=ft.MarkdownCodeTheme.GOOGLE_CODE,
            on_tap_link=lambda e: page.launch_url(e.data),
            expand=True,
        )
    else:
        ask_button = ft.Container()
    
    # 检查当前小节是否已完成
    is_section_completed = db.is_section_completed(chapter_name, section_name) if chapter_name else False
    
    # 根据完成状态创建不同的按钮
    if is_section_completed:
        # 已完成状态 - 显示完成标识
        complete_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=28),
                ft.Text("已完成学习", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD, size=18)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=ft.Colors.GREEN_50,
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            border=ft.border.all(2, ft.Colors.GREEN),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.Colors.GREEN_300,
                offset=ft.Offset(0, 2)
            )
        )
    else:
        # 未完成状态 - 显示完成按钮
        complete_button = ft.ElevatedButton(
            "完成学习",
            on_click=show_completion_dialog,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            icon=ft.Icons.CHECK_CIRCLE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                shadow_color=ft.Colors.GREEN_300,
                elevation=4
            ),
            height=56
        )
    left_width = 600
    study_content = ft.Container(
        content=ft.ListView(
            controls=[
                # 学习内容区域
                ft.Container(
                    content=ft.Markdown(
                        md_content,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme=ft.MarkdownCodeTheme.GOOGLE_CODE,
                        on_tap_link=lambda e: page.launch_url(e.data),
                        expand=True,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.BLACK26,
                        offset=ft.Offset(0, 2)
                    )
                ),
                
                ft.Container(height=20),
                
                # 代码区域
                ft.Container(
                    content=code_alert,
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                ),
                
                ft.Container(height=20),
                
                # 代码运行器
                ft.Container(
                    content=code_runner,
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.Colors.BLACK12,
                        offset=ft.Offset(0, 1)
                    )
                ),
                
                ft.Container(height=20),
                
                # AI评价按钮
                ft.Container(
                    content=ask_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(vertical=10)
                ),
                
                ft.Container(height=20),
                
                # 完成学习按钮区域
                ft.Container(
                    content=complete_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50 if not is_section_completed else ft.Colors.GREEN_50,
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.GREY_300 if not is_section_completed else ft.Colors.GREEN)
                )
            ],
            expand=True,
            padding=ft.padding.all(20),
            spacing=0,
            auto_scroll=False,
        ),
        bgcolor=ft.Colors.GREY_100,
        border_radius=16,
        width=left_width,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=12,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4)
        )
    )

    # -------- 新增：左右可拖动分割 --------


    def update_width(e: ft.DragUpdateEvent):
        nonlocal left_width
        left_width = max(300, int(left_width + e.delta_x))
        study_content.width = left_width
        page.update()

    drag_bar = ft.GestureDetector(
        drag_interval=10,
        on_pan_update=update_width,
        content=ft.Container(
            width=8,
            bgcolor=ft.Colors.GREY_300,
            border_radius=ft.border_radius.all(4),
        ),
    )

    layout = ft.Row(
        controls=[study_content, drag_bar, chat_content],
        expand=True,
    )

    # 设置页面背景色
    page.bgcolor = ft.Colors.GREY_100
    
    page.add(layout)
    page.update()
