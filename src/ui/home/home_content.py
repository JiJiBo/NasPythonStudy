import os
import re
import flet as ft
from typing import Optional
from flet.core.list_tile import ListTile
from datetime import datetime

from src.str.APP_CONFIG import STUDY_DIR
from src.ui.study.study_pagel import study_page
from src.utils.CN2AN_Utils import extract_number
from src.db.study_progress_db import StudyProgressDB


def natural_key(text: str):
    """
    自然排序 key，优先按数字排序，其次按文本
    """
    return [extract_number(text), text]


def format_completion_time(timestamp_str: str) -> str:
    """
    格式化完成时间显示
    """
    if not timestamp_str:
        return ""
    
    try:
        # 解析时间戳
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        # 格式化为更友好的显示
        return dt.strftime("%m-%d %H:%M")
    except:
        return timestamp_str[:16] if timestamp_str else ""


class HomeContent(ft.Column):
    """
    首页内容组件，支持加载本地课件目录，按自然顺序排序（支持中文数字）
    """

    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self._is_mounted = False
        self.load_dir = STUDY_DIR  # 课件目录
        self.db = StudyProgressDB("study_progress.db")  # 初始化学习进度数据库
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
                # 获取章节完成统计
                completed_count = self.db.get_chapter_completed_count(chapter)
                total_sections = len([s for s in os.listdir(chapter_path) 
                                    if os.path.isdir(os.path.join(chapter_path, s))])
                
                # 构建章节标题和副标题
                chapter_title = ft.Text(chapter, weight=ft.FontWeight.BOLD, size=16)
                chapter_subtitle = ft.Text(
                    f"已完成 {completed_count}/{total_sections} 个小节", 
                    size=12, 
                    color=ft.Colors.GREY
                )
                
                # 章节状态图标
                if completed_count == total_sections and total_sections > 0:
                    chapter_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=28, color=ft.Colors.GREEN)
                elif completed_count > 0:
                    chapter_icon = ft.Icon(ft.Icons.PLAY_CIRCLE_FILL, size=28, color=ft.Colors.ORANGE)
                else:
                    chapter_icon = ft.Icon(ft.Icons.BOOK, size=28, color=ft.Colors.BLUE)
                
                # 折叠面板
                chapter_panel = ft.ExpansionTile(
                    leading=chapter_icon,
                    title=chapter_title,
                    subtitle=chapter_subtitle,
                    controls=[]
                )

                # 遍历小节
                for section in sorted(os.listdir(chapter_path), key=natural_key):
                    section_path = os.path.join(chapter_path, section)
                    if os.path.isdir(section_path):
                        # 获取小节学习状态
                        section_status = self.db.get_section_status(chapter, section)
                        is_completed = section_status["is_completed"]
                        completed_time = section_status["completed_timestamp"]
                        
                        # 小节状态图标
                        if is_completed:
                            section_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=22, color=ft.Colors.GREEN)
                        else:
                            section_icon = ft.Icon(ft.Icons.ARTICLE, size=22, color=ft.Colors.GREY)
                        
                        # 小节标题
                        section_title = ft.Text(section, size=14, weight=ft.FontWeight.W_500)
                        
                        # 小节副标题（显示完成时间）
                        if is_completed and completed_time:
                            time_str = format_completion_time(completed_time)
                            section_subtitle = ft.Text(f"已完成 - {time_str}", size=11, color=ft.Colors.GREEN)
                        else:
                            section_subtitle = ft.Text("未完成", size=11, color=ft.Colors.GREY)
                        
                        # 创建小节列表项
                        section_tile = ListTile(
                            leading=section_icon,
                            title=section_title,
                            subtitle=section_subtitle,
                            on_click=lambda e, sp=section_path: study_page(sp, self.page, on_back=self.on_back)
                        )
                        
                        chapter_panel.controls.append(section_tile)

                self.controls.append(chapter_panel)

        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10

    def refresh_ui(self):
        """刷新UI，重新加载学习进度"""
        self._build_ui()
        if self.page:
            self.page.update()

    def did_mount(self):
        self._is_mounted = True

    def will_unmount(self):
        self._is_mounted = False
