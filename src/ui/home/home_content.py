import os
import re
import flet as ft
from typing import Optional
from flet.core.list_tile import ListTile

from src.str.APP_CONFIG import STUDY_DIR
from src.ui.study.study_pagel import study_page
from src.utils.CN2AN_Utils import extract_number


def natural_key(text: str):
    """
    自然排序 key，优先按数字排序，其次按文本
    """
    return [extract_number(text), text]


class HomeContent(ft.Column):
    """
    首页内容组件，支持加载本地课件目录，按自然顺序排序（支持中文数字）
    """

    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self._is_mounted = False
        self.load_dir = STUDY_DIR  # 课件目录
        self._build_ui()

    def _build_ui(self):
        """构建UI，加载章节"""
        self.controls = []

        if not os.path.exists(self.load_dir):
            self.controls.append(ft.Text("课件目录不存在", color=ft.Colors.RED))
            return

        # 遍历章节
        for chapter in sorted(os.listdir(self.load_dir), key=natural_key):
            chapter_path = os.path.join(self.load_dir, chapter)
            if os.path.isdir(chapter_path):
                # 折叠面板
                chapter_panel = ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.BOOK, size=28, color=ft.Colors.BLUE),
                    title=ft.Text(chapter, weight=ft.FontWeight.BOLD, size=16),
                    subtitle=ft.Text("点击展开章节内容", size=12, color=ft.Colors.GREY),
                    controls=[]
                )

                # 遍历小节
                for section in sorted(os.listdir(chapter_path), key=natural_key):
                    section_path = os.path.join(chapter_path, section)
                    if os.path.isdir(section_path):
                        chapter_panel.controls.append(
                            ListTile(
                                leading=ft.Icon(ft.Icons.ARTICLE, size=22, color=ft.Colors.GREEN),
                                title=ft.Text(section, size=14, weight=ft.FontWeight.W_500),
                                on_click=lambda e, sp=section_path: study_page(sp,self.page, on_back=self.on_back)
                            )
                        )

                self.controls.append(chapter_panel)

        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10

    def did_mount(self):
        self._is_mounted = True

    def will_unmount(self):
        self._is_mounted = False
