import flet as ft
import threading
import subprocess
import sys
import os
import webbrowser

from src.str.APP_CONFIG import kvUtils
from src.ui.llm.llm_settings import llm_setting_page
from src.utils.SystemInfo import get_system_info, format_system_info


class SettingItem(ft.Control):
    """
    通用设置项控件（使用 ListTile 实现）
    """

    def __init__(self, icon: str, title: str, description: str = "", on_click=None):
        super().__init__()
        self.icon = icon
        self.title = title
        self.description = description
        self.on_click = on_click

    def build(self):
        return ft.ListTile(
            leading=ft.Icon(self.icon, size=30),
            title=ft.Text(self.title, weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(self.description, size=12, color=ft.Colors.GREY),
            on_click=self.on_click,
            content_padding=ft.Padding(5, 5, 5, 5)
        )


class SettingContent(ft.Column):
    """
    设置页内容
    """

    def __init__(self, page: ft.Page, on_back=None):
        super().__init__()
        self.p = page
        self.on_back = on_back
        self._build_ui()

    def _build_ui(self):
        self.controls = [
            # 大模型设置
            ft.ListTile(
                leading=ft.Icon(ft.Icons.BRANDING_WATERMARK, size=30),
                title=ft.Text("大模型设置", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("配置DeepSeek、Ollama的LLM服务", size=12, color=ft.Colors.GREY),
                on_click=lambda e: llm_setting_page(self.p, on_back=self.on_back),
            ),
            # 聊天记录历史条数设置
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HISTORY, size=30),
                title=ft.Text("聊天记录条数", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("聊天会加载几条历史记录，当作记忆？", size=12, color=ft.Colors.GREY),
                on_click=self._open_history_setting,
            ),
            # 捐款支持
            ft.ListTile(
                leading=ft.Icon(ft.Icons.FAVORITE, size=30, color=ft.Colors.RED),
                title=ft.Text("支持开发者", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("如果这个应用对您有帮助，请考虑支持一下", size=12, color=ft.Colors.GREY),
                on_click=self._open_donation_dialog,
            ),
            # GitHub项目链接
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CODE, size=30, color=ft.Colors.BLACK),
                title=ft.Text("GitHub项目", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("查看项目源码，给个Star支持一下", size=12, color=ft.Colors.GREY),
                on_click=self._open_github_link,
            ),
            # # 应用更新
            # ft.ListTile(
            #     leading=ft.Icon(ft.Icons.UPDATE, size=30),
            #     title=ft.Text("应用更新", weight=ft.FontWeight.BOLD),
            #     subtitle=ft.Text("检查并更新应用版本", size=12, color=ft.Colors.GREY),
            #     on_click=self._open_update_manager,
            # ),
            # # 系统信息
            # ft.ListTile(
            #     leading=ft.Icon(ft.Icons.INFO, size=30),
            #     title=ft.Text("系统信息", weight=ft.FontWeight.BOLD),
            #     subtitle=ft.Text("查看系统信息", size=12, color=ft.Colors.GREY),
            #     on_click=self._open_system_info_dialog,
            # ),
        ]
        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

    def _open_history_setting(self, e):
        max_load_history = kvUtils.get_int("max_load_history", default=20)

        # 弹出对话框输入数字
        def on_submit(e):
            try:
                value = int(tf.value)
                print("设置聊天记录条数为:", value)
                kvUtils.put_int("max_load_history", value)
                self.p.close(dlg_modal)
            except ValueError:
                tf.error_text = "请输入整数"
                dlg_modal.update()

        tf = ft.TextField(value=str(max_load_history), label="历史条数", hint_text="输入整数", width=150)
        dlg_modal = ft.AlertDialog(
            title=ft.Text("设置聊天记录历史条数"),
            content=tf,
            actions=[ft.TextButton("确认", on_click=on_submit),
                     ft.TextButton("取消", on_click=lambda e: self.p.close(dlg_modal))],
            modal=True,
        )
        self.p.dialog = dlg_modal
        self.p.open(dlg_modal)
        self.p.update()

    def _open_donation_dialog(self, e):
        """打开捐款支持对话框"""
        # 创建捐款信息内容
        donation_content = ft.Column([
            ft.Text("💝 支持开发者", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            ft.Text("如果 Aithon 对您的学习有帮助，请考虑支持一下开发工作！", 
                   size=14, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_700),
            ft.Container(height=20),
            
            # 支付宝二维码
            ft.Container(
                content=ft.Column([
                    ft.Text("支付宝", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text("扫码支持", size=12, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.BLUE_600,
                        padding=ft.Padding(10, 5, 10, 5),
                        border_radius=5,
                        width=100,
                        alignment=ft.alignment.center
                    ),
                     ft.Image("assets/coffee/支付宝.JPG", width=360, height=360, fit=ft.ImageFit.CONTAIN),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=20,
                width=400,
                height=480
            ),
            
            ft.Container(height=20),
            
            # 微信二维码
            ft.Container(
                content=ft.Column([
                    ft.Text("微信", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text("扫码支持", size=12, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_600,
                        padding=ft.Padding(10, 5, 10, 5),
                        border_radius=5,
                        width=100,
                        alignment=ft.alignment.center
                    ),
                     ft.Image("assets/coffee/微信.JPG", width=360, height=360, fit=ft.ImageFit.CONTAIN),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=20,
                width=400,
                height=480
            ),
            
            ft.Container(height=20),
            
            # 感谢信息
            ft.Container(
                content=ft.Text("🙏 感谢您的支持！\n您的支持是我继续开发的动力", 
                              size=14, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_700),
                bgcolor=ft.Colors.YELLOW_50,
                border=ft.border.all(1, ft.Colors.YELLOW_200),
                border_radius=10,
                padding=15
            ),
            
            ft.Container(height=10),
            
            # 其他支持方式
            ft.Text("其他支持方式：", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("• 给项目点个 ⭐ Star", size=12, color=ft.Colors.GREY_700),
            ft.Text("• 分享给更多需要的人", size=12, color=ft.Colors.GREY_700),
            ft.Text("• 反馈使用体验和建议", size=12, color=ft.Colors.GREY_700),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        # 创建对话框
        dialog = ft.AlertDialog(
            title=ft.Text("支持开发者", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=donation_content,
                width=600,
                height=1000,
                padding=10
            ),
            actions=[
                ft.TextButton("关闭", on_click=lambda e: self.p.close(dialog))
            ],
            modal=True
        )
        
        self.p.dialog = dialog
        self.p.open(dialog)
        self.p.update()

    def _open_github_link(self, e):
        """打开GitHub项目链接"""
        github_url = "https://github.com/JiJiBo/NasPythonStudy.git"
        try:
            webbrowser.open(github_url)
        except Exception as ex:
            # 如果无法打开浏览器，显示错误信息
            error_dialog = ft.AlertDialog(
                title=ft.Text("打开链接失败"),
                content=ft.Text(f"无法打开浏览器，请手动访问：\n{github_url}"),
                actions=[
                    ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))
                ]
            )
            self.p.dialog = error_dialog
            self.p.open(error_dialog)
            self.p.update()

    def _open_system_info_dialog(self, e):
        """打开系统信息对话框"""
        # 创建加载状态组件
        loading_text = ft.Text("正在检测系统信息...", size=14, color=ft.Colors.BLUE)
        loading_progress = ft.ProgressBar(width=400, visible=True)
        loading_container = ft.Container(
            content=ft.Column([
                loading_text,
                loading_progress
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )

        # 创建对话框
        dialog = ft.AlertDialog(
            title=ft.Text("系统信息"),
            content=loading_container,
            actions=[
                ft.TextButton("关闭", on_click=lambda e: self.p.close(dialog))
            ]
        )

        self.p.dialog = dialog
        self.p.open(dialog)
        self.p.update()

        # 在后台线程中获取系统信息
        def get_info():
            try:
                system_info = get_system_info()
                formatted_info = format_system_info(system_info)
                
                # 更新UI
                def update_ui():
                    dialog.content = ft.Container(
                        content=ft.Column([
                            ft.Text("系统信息", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text(formatted_info, size=12, selectable=True)
                        ], scroll=ft.ScrollMode.AUTO),
                        padding=20,
                        width=500,
                        height=400
                    )
                    self.p.update()

                # 在主线程中更新UI
                self.p.run_thread(update_ui)

            except Exception as ex:
                def show_error():
                    dialog.content = ft.Container(
                        content=ft.Text(f"获取系统信息失败: {str(ex)}", color=ft.Colors.RED),
                        padding=20
                    )
                    self.p.update()

                self.p.run_thread(show_error)

        # 启动后台线程
        threading.Thread(target=get_info, daemon=True).start()

    def _open_update_manager(self, e):
        """打开更新管理器对话框"""
        from src.utils.UpdateManager import update_manager
        
        # 创建更新状态显示组件
        status_text = ft.Text("正在检查更新...", size=14, color=ft.Colors.BLUE)
        progress_bar = ft.ProgressBar(width=400, visible=False)
        update_button = ft.ElevatedButton("检查更新", disabled=True)
        version_text = ft.Text("", size=12, color=ft.Colors.GREY)
        
        # 创建对话框
        dialog = ft.AlertDialog(
            title=ft.Text("应用更新"),
            content=ft.Container(
                content=ft.Column([
                    status_text,
                    version_text,
                    progress_bar,
                    update_button
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                width=400
            ),
            actions=[
                ft.TextButton("关闭", on_click=lambda e: self.p.close(dialog))
            ]
        )
        
        def update_ui():
            """更新UI状态"""
            self.p.update()
        
        def check_updates():
            """检查更新"""
            try:
                # 更新状态文本
                status_text.value = "正在检查应用更新..."
                update_ui()
                
                # 检查应用更新
                app_update = update_manager.check_app_update()
                
                if app_update and app_update.get("has_update"):
                    status_text.value = f"发现新版本: {app_update['remote_version']}"
                    status_text.color = ft.Colors.GREEN
                    version_text.value = f"当前版本: {app_update['current_version']} → 新版本: {app_update['remote_version']}"
                    
                    # 启用更新按钮
                    update_button.disabled = False
                    update_button.text = "立即更新"
                    update_button.on_click = lambda e: start_update(app_update)
                else:
                    status_text.value = "已是最新版本"
                    status_text.color = ft.Colors.GREEN
                    version_text.value = f"当前版本: {update_manager.update_config.get('current_version', '未知')}"
                
                update_ui()
                
            except Exception as ex:
                status_text.value = f"检查更新失败: {str(ex)}"
                status_text.color = ft.Colors.RED
                update_ui()
        
        def start_update(app_update):
            """开始更新"""
            try:
                status_text.value = "正在下载更新..."
                status_text.color = ft.Colors.BLUE
                progress_bar.visible = True
                progress_bar.value = 0
                update_button.disabled = True
                update_button.text = "更新中..."
                update_ui()
                
                def progress_callback(update_type, progress, downloaded, total):
                    """更新进度回调"""
                    progress_bar.value = progress / 100
                    status_text.value = f"下载进度: {progress:.1f}% ({downloaded//1024//1024}MB/{total//1024//1024}MB)"
                    update_ui()
                
                def error_callback(error_msg):
                    """错误回调"""
                    status_text.value = f"更新失败: {error_msg}"
                    status_text.color = ft.Colors.RED
                    progress_bar.visible = False
                    update_button.disabled = False
                    update_button.text = "重试"
                    update_ui()
                
                # 开始下载更新
                update_url = app_update.get("update_url")
                if update_url:
                    success = update_manager.download_app_update(
                        update_url, progress_callback, error_callback
                    )
                    if success:
                        status_text.value = "更新下载完成，请重启应用"
                        status_text.color = ft.Colors.GREEN
                        progress_bar.visible = False
                        update_ui()
                
            except Exception as ex:
                error_callback(str(ex))
        
        # 显示对话框
        self.p.dialog = dialog
        self.p.open(dialog)
        self.p.update()
        
        # 启动检查更新线程
        threading.Thread(target=check_updates, daemon=True).start()