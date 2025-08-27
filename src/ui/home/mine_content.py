import flet as ft
from typing import Callable, Optional


class MineContent(ft.Column):
    """
    具有生命周期的首页内容组件
    """

    def __init__(self, on_button_click: Optional[Callable] = None):
        super().__init__()
        self.on_button_click_callback = on_button_click or self.default_button_click
        self._is_mounted = False

        # 初始化组件
        self._build_ui()

    def _build_ui(self):
        """构建UI组件"""
        self.controls = [
            ft.Icon(ft.Icons.HOME, size=50, color=ft.Colors.GREEN_700),
            ft.Text("欢迎使用我的应用", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("这是主页内容区域", size=16, color=ft.Colors.GREY_600),
            ft.ElevatedButton(
                "了解更多",
                icon=ft.Icons.INFO,
                on_click=self._on_button_click
            ),
            ft.Text("状态: 未加载", size=12, color=ft.Colors.GREY )
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

    def did_mount(self):
        """组件挂载到页面时调用"""
        self._is_mounted = True
        self._update_status("组件已加载")
        print("MineContent: 组件已挂载")

        # 模拟数据加载
        self._load_data()

    def will_unmount(self):
        """组件从页面卸载时调用"""
        self._is_mounted = False
        self._update_status("组件已卸载")
        print("MineContent: 组件即将卸载")

        # 清理资源
        self._cleanup()

    def _load_data(self):
        """模拟数据加载"""
        if not self._is_mounted:
            return

        self._update_status("正在加载数据...")

        # 模拟异步数据加载
        def load_complete():
            if self._is_mounted:
                self._update_status("数据加载完成")
                # 添加加载完成后的UI更新
                if len(self.controls) == 5:  # 只有初始控件时
                    self.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text("最新动态:", weight=ft.FontWeight.BOLD),
                                ft.Text("• 系统更新完成"),
                                ft.Text("• 新增3个功能"),
                                ft.Text("• 优化了用户体验"),
                            ], spacing=5),
                            padding=10,
                            bgcolor=ft.Colors.GREEN_50,
                            border_radius=10
                        )
                    )
                    self.update()

        # 模拟延迟加载
        import threading
        timer = threading.Timer(2.0, load_complete)
        timer.daemon = True
        timer.start()

    def _cleanup(self):
        """清理资源"""
        print("MineContent: 执行清理操作")
        # 这里可以取消定时器、关闭连接等

    def _update_status(self, message: str):
        """更新状态文本"""
        if self._is_mounted:
            status_text = self.get_status_text()
            if status_text:
                status_text.value = f"状态: {message}"
                self.update()

    def get_status_text(self) -> Optional[ft.Text]:
        """获取状态文本控件"""
        for control in self.controls:
            if hasattr(control, 'id') and control.id == "status_text":
                return control
        return None

    def _on_button_click(self, e):
        """按钮点击事件处理"""
        if self._is_mounted:
            self._update_status("按钮被点击")
            print("MineContent: 按钮被点击")
            self.on_button_click_callback(e)

    def default_button_click(self, e):
        """默认按钮点击处理"""
        # 显示点击反馈
        button = e.control
        original_bgcolor = button.bgcolor

        # 动画效果
        button.bgcolor = ft.Colors.GREEN_100
        self.update()

        # 添加临时提示
        import threading
        def reset_button():
            if self._is_mounted:
                button.bgcolor = original_bgcolor
                self.update()

        timer = threading.Timer(0.3, reset_button)
        timer.daemon = True
        timer.start()

    def refresh_data(self):
        """外部调用：刷新数据"""
        if self._is_mounted:
            print("MineContent: 手动刷新数据")
            self._update_status("正在刷新数据...")

            # 移除动态添加的内容，只保留基本控件
            if len(self.controls) > 5:
                self.controls = self.controls[:5]

            # 重新加载数据
            self._load_data()

