import flet as ft
import threading
import time

from src.ui.view.RitchView import RichContent


class PullToRefreshList(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.refreshing = False
        self.auto_scroll = True
        self.drag_distance = 0

        # 刷新提示
        self.refresh_indicator = ft.Text("下拉刷新...", visible=False)
        self.refresh_indicator_container = ft.GestureDetector(
            content=self.refresh_indicator,
            on_vertical_drag_update=self.on_drag,
            on_vertical_drag_end=self.on_drag_end
        )

        # 列表内容
        self.list_view = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

        # 添加到 Column
        self.controls = [
            # self.refresh_indicator_container,
            self.list_view
        ]

    def on_drag(self, e):
        self.drag_distance += e.delta_y
        if self.drag_distance > 50 and not self.refreshing:
            self.refreshing = True
            self.refresh_indicator.visible = True
            self.update()
            self.refresh_data()

    def on_drag_end(self, e):
        self.drag_distance = 0

    def refresh_data(self):
        def do_refresh():
            print("刷新数据中...")
            time.sleep(1)  # 模拟网络请求
            self.refresh_indicator.visible = False
            self.refreshing = False
            self.update()

            if self.auto_scroll:
                self.scroll_to_bottom()

        threading.Thread(target=do_refresh).start()

    def add_item(self, item):
        self.list_view.controls.append(RichContent(item))
        self.update()
        if self.auto_scroll:
            self.scroll_to_bottom()

    def scroll_to_bottom(self, e=None):
        # 滚动到底部
        self.list_view.scroll_to(offset=0)
        self.auto_scroll = True

        # 在这里可以调用 AI 回复逻辑
