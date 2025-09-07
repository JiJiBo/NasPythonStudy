import flet as ft
import threading
import subprocess
import sys
import os

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
                subtitle=ft.Text("配置OpenAI、DeepSeek、Ollama、本地模型等LLM服务", size=12, color=ft.Colors.GREY),
                on_click=lambda e: llm_setting_page(self.p, on_back=self.on_back),
            ),
            # 本地模型管理
            ft.ListTile(
                leading=ft.Icon(ft.Icons.STORAGE, size=30),
                title=ft.Text("本地模型管理", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("下载、管理和切换本地AI模型", size=12, color=ft.Colors.GREY),
                on_click=self._open_local_model_manager,
            ),
            # 聊天记录历史条数设置
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HISTORY, size=30),
                title=ft.Text("聊天记录条数", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("聊天会加载几条历史记录，当作记忆？", size=12, color=ft.Colors.GREY),
                on_click=self._open_history_setting,
            ),
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
    
    def _open_local_model_manager(self, e):
        """打开本地模型管理页面"""
        from src.utils.LocalModelManager import local_model_manager
        
        # 创建模型管理对话框
        def create_model_list():
            available_models = local_model_manager.get_available_models()
            installed_models = local_model_manager.get_installed_models()
            installed_names = [m.name for m in installed_models]
            current_model = local_model_manager.current_model
            
            model_list = []
            for model_name, model_info in available_models.items():
                is_installed = model_name in installed_names
                is_current = model_name == current_model
                size_mb = model_info.size // (1024 * 1024)
                
                status_text = ""
                if is_current:
                    status_text = "✓ 当前使用"
                elif is_installed:
                    status_text = "✓ 已安装"
                else:
                    status_text = "未安装"
                
                model_list.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MEMORY, size=24),
                        title=ft.Text(model_name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{size_mb}MB - {model_info.description} - {status_text}", 
                                       size=12, color=ft.Colors.GREY),
                        trailing=ft.Row([
                            ft.ElevatedButton(
                                "下载" if not is_installed else "加载" if not is_current else "已加载",
                                on_click=lambda e, name=model_name: self._handle_model_action(name, is_installed, is_current),
                                disabled=is_current
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                on_click=lambda e, name=model_name: self._delete_model(name),
                                disabled=not is_installed or is_current,
                                tooltip="删除模型"
                            )
                        ], spacing=5),
                        content_padding=ft.Padding(5, 5, 5, 5)
                    )
                )
            
            return model_list
        
        def refresh_dialog():
            dialog.content = ft.Container(
                content=ft.Column([
                    ft.Text("本地模型管理", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column(create_model_list(), scroll=ft.ScrollMode.AUTO)
                ]),
                padding=20,
                width=600,
                height=500
            )
            self.p.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("本地模型管理"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("正在加载模型列表...", size=14, color=ft.Colors.BLUE)
                ]),
                padding=20,
                width=600,
                height=500
            ),
            actions=[
                ft.TextButton("刷新", on_click=lambda e: refresh_dialog()),
                ft.TextButton("关闭", on_click=lambda e: self.p.close(dialog))
            ]
        )
        
        self.p.dialog = dialog
        self.p.open(dialog)
        self.p.update()
        
        # 延迟加载模型列表
        def load_models():
            import time
            time.sleep(0.5)  # 短暂延迟让用户看到加载状态
            self.p.run_thread(refresh_dialog)
        
        threading.Thread(target=load_models, daemon=True).start()
    
    def _handle_model_action(self, model_name, is_installed, is_current):
        """处理模型操作（下载或加载）"""
        from src.utils.LocalModelManager import local_model_manager
        
        if not is_installed:
            # 下载模型
            def progress_callback(name, progress, downloaded, total):
                self.p.snack_bar = ft.SnackBar(
                    ft.Text(f"下载 {name}: {progress:.1f}% ({downloaded//1024//1024}MB/{total//1024//1024}MB)")
                )
                self.p.snack_bar.open = True
                self.p.update()
            
            def error_callback(error):
                self.p.snack_bar = ft.SnackBar(ft.Text(f"下载失败: {error}"))
                self.p.snack_bar.open = True
                self.p.update()
            
            local_model_manager.download_model(model_name, progress_callback, error_callback)
        else:
            # 加载模型
            if local_model_manager.load_model(model_name):
                self.p.snack_bar = ft.SnackBar(ft.Text(f"已加载模型: {model_name}"))
            else:
                self.p.snack_bar = ft.SnackBar(ft.Text(f"加载模型失败: {model_name}"))
            self.p.snack_bar.open = True
            self.p.update()
    
    def _delete_model(self, model_name):
        """删除模型"""
        from src.utils.LocalModelManager import local_model_manager
        
        def confirm_delete(e):
            if local_model_manager.delete_model(model_name):
                self.p.snack_bar = ft.SnackBar(ft.Text(f"已删除模型: {model_name}"))
            else:
                self.p.snack_bar = ft.SnackBar(ft.Text("删除失败"))
            self.p.snack_bar.open = True
            self.p.close(confirm_dlg)
            self.p.update()
        
        confirm_dlg = ft.AlertDialog(
            title=ft.Text("确认删除"),
            content=ft.Text(f"确定要删除模型 {model_name} 吗？此操作不可恢复。"),
            actions=[
                ft.TextButton("删除", on_click=confirm_delete),
                ft.TextButton("取消", on_click=lambda e: self.p.close(confirm_dlg))
            ]
        )
        
        self.p.dialog = confirm_dlg
        self.p.open(confirm_dlg)
        self.p.update()