import flet as ft
import threading
import subprocess
import sys
import os

from src.str.APP_CONFIG import kvUtils
from src.ui.llm.llm_settings import llm_setting_page
from src.utils.SystemInfo import get_system_info, format_system_info
from src.utils.DownloadManager import download_manager
from src.utils.UpdateManager import update_manager


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
            # 一键更新
            ft.ListTile(
                leading=ft.Icon(ft.Icons.UPDATE, size=30),
                title=ft.Text("一键更新", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("检查并更新应用和模型", size=12, color=ft.Colors.GREY),
                on_click=self._open_update_manager,
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
        
        # 存储每个模型的进度条和状态文本（改为实例变量）
        if not hasattr(self, 'model_progress_bars'):
            self.model_progress_bars = {}
        if not hasattr(self, 'model_status_texts'):
            self.model_status_texts = {}
        if not hasattr(self, 'model_buttons'):
            self.model_buttons = {}
        
        # 节流机制
        last_update_times = {}
        
        # 订阅下载事件
        def on_download_status_changed(data):
            print(f"收到下载状态变化事件: {data['model_name']}")
            model_name = data["model_name"]
            status_data = data["status"]
            
            if model_name in self.model_progress_bars:
                # 节流：每0.1秒更新一次UI（减少延迟）
                import time
                now = time.time()
                if model_name in last_update_times and now - last_update_times[model_name] < 0.1:
                    print(f"跳过UI更新（节流）: {model_name}")
                    return
                last_update_times[model_name] = now
                
                def update_ui():
                    try:
                        print(f"开始更新UI: {model_name}")
                        progress_bar = self.model_progress_bars[model_name]
                        status_text = self.model_status_texts[model_name]
                        button = self.model_buttons[model_name]
                        
                        # 检查控件是否存在且有效
                        if progress_bar and status_text and button:
                            if status_data["status"] == "downloading":
                                progress_bar.visible = True
                                progress_bar.value = status_data["progress"] / 100
                                status_text.value = f"下载中: {status_data['progress']:.1f}% ({status_data['downloaded_size']//1024//1024}MB/{status_data['total_size']//1024//1024}MB)"
                                status_text.color = ft.Colors.BLUE
                                button.text = "暂停"
                                button.disabled = False
                            elif status_data["status"] == "paused":
                                progress_bar.visible = True
                                progress_bar.value = status_data["progress"] / 100
                                status_text.value = f"已暂停: {status_data['progress']:.1f}%"
                                status_text.color = ft.Colors.ORANGE
                                button.text = "恢复"
                                button.disabled = False
                            elif status_data["status"] == "completed":
                                progress_bar.visible = False
                                status_text.value = "✓ 下载完成"
                                status_text.color = ft.Colors.GREEN
                                button.text = "已安装"
                                button.disabled = True
                            elif status_data["status"] == "error":
                                progress_bar.visible = False
                                status_text.value = f"下载失败: {status_data['error_message']}"
                                status_text.color = ft.Colors.RED
                                button.text = "重试"
                                button.disabled = False
                            
                            # 更新所有控件
                            progress_bar.update()
                            status_text.update()
                            button.update()
                            
                            # 更新父容器确保UI刷新
                            if hasattr(self, '_model_list_column') and self._model_list_column:
                                self._model_list_column.update()
                            
                            print(f"✅ UI更新完成: {model_name} - {status_data['status']} - {status_data['progress']:.1f}%")
                    except Exception as e:
                        print(f"❌ UI更新错误: {e}")
                
                # 使用try-catch包装，避免阻塞
                try:
                    self.p.run_thread(update_ui)
                    print(f"UI更新线程已启动: {model_name}")
                except Exception as e:
                    print(f"启动UI更新线程失败: {e}")
                    # 如果run_thread失败，直接调用update_ui
                    try:
                        update_ui()
                    except Exception as e2:
                        print(f"直接UI更新也失败: {e2}")
        
        # 取消之前的订阅（如果有的话）
        if hasattr(self, '_download_callback'):
            download_manager.unsubscribe_download_events(self._download_callback)
        
        # 保存回调引用并订阅下载事件
        self._download_callback = on_download_status_changed
        download_manager.subscribe_download_events(on_download_status_changed)
        
        # 状态同步函数
        def sync_download_status():
            """同步下载状态到UI"""
            print("同步下载状态到UI")
            for model_name in self.model_progress_bars.keys():
                print(model_name,self.model_progress_bars.keys())
                try:
                    progress_bar = self.model_progress_bars[model_name]
                    status_text = self.model_status_texts[model_name]
                    button = self.model_buttons[model_name]
                    status = download_manager.get_download_status(model_name)
                    print(f"模型 {model_name} 的下载状态: {status}")
                    
                    if status and progress_bar and status_text and button:
                        if status.status == "downloading":
                            progress_bar.visible = True
                            progress_bar.value = status.progress / 100
                            status_text.value = f"下载中: {status.progress:.1f}% ({status.downloaded_size//1024//1024}MB/{status.total_size//1024//1024}MB)"
                            status_text.color = ft.Colors.BLUE
                            button.text = "暂停"
                            button.disabled = False
                        elif status.status == "paused":
                            progress_bar.visible = True
                            progress_bar.value = status.progress / 100
                            status_text.value = f"已暂停: {status.progress:.1f}%"
                            status_text.color = ft.Colors.ORANGE
                            button.text = "恢复"
                            button.disabled = False
                        elif status.status == "completed":
                            progress_bar.visible = False
                            status_text.value = "✓ 下载完成"
                            status_text.color = ft.Colors.GREEN
                            button.text = "已安装"
                            button.disabled = True
                        elif status.status == "error":
                            progress_bar.visible = False
                            status_text.value = f"下载失败: {status.error_message}"
                            status_text.color = ft.Colors.RED
                            button.text = "重试"
                            button.disabled = False
                        
                        # 更新所有控件
                        progress_bar.update()
                        status_text.update()
                        button.update()
                        
                        print(f"🔄 同步状态: {model_name} - {status.status} - {status.progress:.1f}%")
                    else:
                        # 没有下载状态，检查是否已安装
                        print(f"模型 {model_name} 没有下载状态，检查安装状态")
                        if progress_bar and status_text and button:
                            progress_bar.visible = False
                            progress_bar.value = 0
                            
                            # 检查模型是否已安装
                            from src.utils.LocalModelManager import local_model_manager
                            is_installed = local_model_manager.is_model_installed(model_name)
                            
                            if is_installed:
                                status_text.value = "✓ 已下载"
                                status_text.color = ft.Colors.GREEN
                                button.text = "已下载"
                                button.disabled = True
                            else:
                                status_text.value = "未下载"
                                status_text.color = ft.Colors.GREY
                                button.text = "下载"
                                button.disabled = False
                            
                            progress_bar.update()
                            status_text.update()
                            button.update()
                            
                            print(f"🔄 设置状态: {model_name} - {'已下载' if is_installed else '未下载'}")
                except Exception as e:
                    print(f"❌ 同步状态错误 {model_name}: {e}")
            
            # 更新父容器确保UI刷新
            if hasattr(self, '_model_list_column') and self._model_list_column:
                self._model_list_column.update()
                print("✅ 父容器已更新")
        
        # 保存同步函数引用，供其他方法使用
        self._sync_download_status = sync_download_status
        
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
                
                # 检查下载状态
                download_status = download_manager.get_download_status(model_name)
                
                status_text = ""
                button_text = "下载"
                button_disabled = False
                
                if download_status:
                    if download_status.status == "downloading":
                        status_text = f"下载中: {download_status.progress:.1f}%"
                        button_text = "暂停"
                    elif download_status.status == "paused":
                        status_text = f"已暂停: {download_status.progress:.1f}%"
                        button_text = "恢复"
                    elif download_status.status == "completed":
                        status_text = "✓ 下载完成"
                        button_text = "已安装"
                        button_disabled = True
                    elif download_status.status == "error":
                        status_text = f"下载失败: {download_status.error_message}"
                        button_text = "重试"
                elif is_current:
                    status_text = "✓ 当前使用"
                    button_text = "已加载"
                    button_disabled = True
                elif is_installed:
                    status_text = "✓ 已下载"
                    button_text = "已下载"
                    button_disabled = True
                else:
                    status_text = "未下载"
                
                # 简化模型名称显示
                display_name = model_name.replace("qwen2.5-coder-1.5b-", "Qwen-")
                short_description = model_info.description[:30] + "..." if len(model_info.description) > 30 else model_info.description
                
                # 创建进度条（根据下载状态决定是否显示）
                progress_bar = ft.ProgressBar(
                    width=200,
                    visible=download_status is not None and download_status.status in ["downloading", "paused"],
                    value=(download_status.progress / 100) if download_status else 0,
                    color=ft.Colors.BLUE
                )
                
                # 创建状态文本
                status_text_widget = ft.Text(
                    f"{size_mb}MB - {short_description} - {status_text}", 
                    size=11, 
                    color=ft.Colors.GREY
                )
                
                # 创建下载按钮
                download_btn = ft.ElevatedButton(
                    button_text,
                    disabled=button_disabled,
                    width=80,
                    height=30
                )
                
                # 设置按钮点击事件（避免闭包问题）
                def create_click_handler(name, installed, current, progress, status, button):
                    return lambda e: self._handle_model_action(name, installed, current, progress, status, button)
                
                download_btn.on_click = create_click_handler(model_name, is_installed, is_current, progress_bar, status_text_widget, download_btn)
                
                # 存储引用到实例变量
                self.model_progress_bars[model_name] = progress_bar
                self.model_status_texts[model_name] = status_text_widget
                self.model_buttons[model_name] = download_btn
                
                model_list.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MEMORY, size=24),
                        title=ft.Text(display_name, weight=ft.FontWeight.BOLD, size=14),
                        subtitle=ft.Column([
                            status_text_widget,
                            progress_bar
                        ], spacing=2),
                        trailing=ft.Column([
                            download_btn,
                            ft.IconButton(
                                ft.Icons.DELETE,
                                on_click=lambda e, name=model_name: self._delete_model(name),
                                disabled=not is_installed or is_current,
                                tooltip="删除模型",
                                width=40,
                                height=30
                            )
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        content_padding=ft.Padding(8, 8, 8, 8)
                    )
                )
            
            return model_list
        
        def refresh_dialog():
            # 创建模型列表
            model_list = create_model_list()
            
            # 创建模型列表容器并保存引用
            self._model_list_column = ft.Column(model_list, scroll=ft.ScrollMode.AUTO)
            
            dialog.content = ft.Container(
                content=ft.Column([
                    ft.Text("本地模型管理", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Container(
                        content=self._model_list_column,
                        width=700,
                        height=400
                    )
                ]),
                padding=ft.Padding(20, 20, 20, 20),
                width=750,
                height=500
            )
            self.p.update()
            
            # 刷新后同步下载状态
            def sync_after_refresh():
                import time
                time.sleep(0.2)  # 等待UI更新完成
                sync_download_status()
            
            self.p.run_thread(sync_after_refresh)
        
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
                ft.TextButton("关闭", on_click=lambda e: self._close_model_dialog(dialog))
            ]
        )
        
        self.p.dialog = dialog
        self.p.open(dialog)
        self.p.update()
        
        # 延迟加载模型列表，确保对话框完全打开
        def load_models():
            import time
            time.sleep(0.8)  # 增加延迟确保对话框完全打开
            self.p.run_thread(refresh_dialog)
        
        threading.Thread(target=load_models, daemon=True).start()
    
    def _close_model_dialog(self, dialog):
        """关闭模型管理对话框并取消订阅"""
        # 取消下载事件订阅
        if hasattr(self, '_download_callback'):
            download_manager.unsubscribe_download_events(self._download_callback)
            delattr(self, '_download_callback')
        
        # 关闭对话框
        self.p.close(dialog)
    
    def _handle_model_action(self, model_name, is_installed, is_current, progress_bar=None, status_text=None, button=None):
        """处理模型操作（下载或加载）"""
        from src.utils.LocalModelManager import local_model_manager
        
        # 如果模型已下载，不允许重复下载
        if is_installed:
            self.p.snack_bar = ft.SnackBar(
                content=ft.Text(f"模型 {model_name} 已下载，无需重复下载"),
                bgcolor=ft.Colors.ORANGE
            )
            self.p.snack_bar.open = True
            self.p.update()
            return
        
        # 检查当前下载状态
        download_status = download_manager.get_download_status(model_name)
        
        if download_status:
            # 有下载状态，根据状态执行操作
            if download_status.status == "downloading":
                # 暂停下载
                download_manager.pause_download(model_name)
                self.p.snack_bar = ft.SnackBar(
                    content=ft.Text(f"已暂停下载 {model_name}"),
                    bgcolor=ft.Colors.ORANGE
                )
                self.p.snack_bar.open = True
                self.p.update()
                
            elif download_status.status == "paused":
                # 恢复下载
                success = download_manager.resume_download(model_name)
                if success:
                    self.p.snack_bar = ft.SnackBar(
                        content=ft.Text(f"恢复下载 {model_name}"),
                        bgcolor=ft.Colors.BLUE
                    )
                    self.p.snack_bar.open = True
                    self.p.update()
                    
                    # 恢复下载后立即同步状态
                    def sync_after_resume():
                        import time
                        time.sleep(0.1)  # 等待状态更新
                        if hasattr(self, '_sync_download_status'):
                            self._sync_download_status()
                    
                    self.p.run_thread(sync_after_resume)
                else:
                    self.p.snack_bar = ft.SnackBar(
                        content=ft.Text(f"恢复下载失败 {model_name}"),
                        bgcolor=ft.Colors.RED
                    )
                    self.p.snack_bar.open = True
                    self.p.update()
                
            elif download_status.status == "error":
                # 重试下载
                download_manager.cancel_download(model_name)
                # 获取下载URL并重新开始
                available_models = local_model_manager.get_available_models()
                if model_name in available_models:
                    model_info = available_models[model_name]
                    download_url = local_model_manager.get_best_mirror_url(model_name)
                    success = download_manager.start_download(model_name, download_url, model_info.size)
                    if success:
                        self.p.snack_bar = ft.SnackBar(
                            content=ft.Text(f"重新开始下载 {model_name}"),
                            bgcolor=ft.Colors.BLUE
                        )
                        self.p.snack_bar.open = True
                        self.p.update()
        elif not is_installed:
            # 开始新下载
            print(f"开始下载模型: {model_name}")
            available_models = local_model_manager.get_available_models()
            if model_name in available_models:
                model_info = available_models[model_name]
                print(f"获取模型信息: {model_name}, 大小: {model_info.size//1024//1024}MB")
                
                download_url = local_model_manager.get_best_mirror_url(model_name)
                print(f"获取下载URL: {download_url}")
                
                try:
                    success = download_manager.start_download(model_name, download_url, model_info.size)
                    print(f"启动下载结果: {success}")
                except Exception as e:
                    print(f"启动下载异常: {e}")
                    success = False
                
                if success:
                    self.p.snack_bar = ft.SnackBar(
                        content=ft.Text(f"开始下载 {model_name}"),
                        bgcolor=ft.Colors.BLUE
                    )
                    self.p.snack_bar.open = True
                    self.p.update()
                    
                    # 下载开始后立即同步状态
                    def sync_after_start():
                        import time
                        time.sleep(0.1)  # 等待下载状态创建
                        if hasattr(self, '_sync_download_status'):
                            self._sync_download_status()
                    
                    self.p.run_thread(sync_after_start)
                else:
                    self.p.snack_bar = ft.SnackBar(
                        content=ft.Text(f"启动下载失败 {model_name}"),
                        bgcolor=ft.Colors.RED
                    )
                    self.p.snack_bar.open = True
                    self.p.update()
        else:
            # 加载模型
            if not is_current:
                self.p.snack_bar = ft.SnackBar(
                    content=ft.Text(f"正在加载模型 {model_name}..."),
                    bgcolor=ft.Colors.BLUE
                )
                self.p.snack_bar.open = True
                self.p.update()
                
                success = local_model_manager.load_model(model_name)
                if success:
                    self.p.snack_bar = ft.SnackBar(
                        content=ft.Text(f"模型 {model_name} 加载成功"),
                        bgcolor=ft.Colors.GREEN
                    )
                else:
                    self.p.snack_bar = ft.SnackBar(
                        content=ft.Text(f"模型 {model_name} 加载失败"),
                        bgcolor=ft.Colors.RED
                    )
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
    
    def _open_update_manager(self, e):
        """打开更新管理器对话框"""
        # 创建更新状态显示组件
        status_text = ft.Text("正在检查更新...", size=14, color=ft.Colors.BLUE)
        progress_bar = ft.ProgressBar(width=400, visible=False)
        
        # 创建更新按钮
        check_update_btn = ft.ElevatedButton(
            "检查更新",
            icon=ft.Icons.REFRESH,
            on_click=lambda e: self._check_updates(status_text, progress_bar, check_update_btn)
        )
        
        # 创建更新信息显示区域
        update_info_container = ft.Container(
            content=ft.Column([
                status_text,
                progress_bar
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10
        )
        
        # 创建对话框
        dialog = ft.AlertDialog(
            title=ft.Text("一键更新"),
            content=ft.Container(
                content=ft.Column([
                    update_info_container,
                    ft.Divider(),
                    check_update_btn
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=500,
                height=300
            ),
            actions=[
                ft.TextButton("关闭", on_click=lambda e: self.p.close(dialog))
            ]
        )
        
        self.p.dialog = dialog
        self.p.open(dialog)
        self.p.update()
        
        # 自动检查更新
        self._check_updates(status_text, progress_bar, check_update_btn)
    
    def _check_updates(self, status_text, progress_bar, check_btn):
        """检查更新"""
        def check_thread():
            try:
                # 更新状态
                def update_status(text, color=ft.Colors.BLUE):
                    status_text.value = text
                    status_text.color = color
                    status_text.update()
                
                # 检查应用更新
                update_status("正在检查应用更新...")
                app_update = update_manager.check_app_update()
                
                # 检查模型更新
                update_status("正在检查模型更新...")
                model_updates = update_manager.check_model_update()
                
                # 显示结果
                has_app_update = app_update and app_update.get("has_update")
                has_model_update = any(info.get("has_update") for info in model_updates.values())
                
                if has_app_update or has_model_update:
                    update_status("发现可用更新！", ft.Colors.ORANGE)
                    self._show_update_options(app_update, model_updates, status_text, progress_bar, check_btn)
                else:
                    update_status("已是最新版本", ft.Colors.GREEN)
                    check_btn.text = "重新检查"
                    check_btn.update()
                    
            except Exception as e:
                status_text.value = f"检查更新失败: {str(e)}"
                status_text.color = ft.Colors.RED
                status_text.update()
        
        # 在后台线程中检查更新
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def _show_update_options(self, app_update, model_updates, status_text, progress_bar, check_btn):
        """显示更新选项"""
        update_buttons = []
        
        # 应用更新按钮
        if app_update and app_update.get("has_update"):
            app_btn = ft.ElevatedButton(
                f"更新应用到 {app_update['remote_version']}",
                icon=ft.Icons.DOWNLOAD,
                on_click=lambda e: self._download_app_update(app_update, status_text, progress_bar)
            )
            update_buttons.append(app_btn)
        
        # 模型更新按钮
        for model_name, update_info in model_updates.items():
            if update_info.get("has_update"):
                model_btn = ft.ElevatedButton(
                    f"更新模型 {model_name}",
                    icon=ft.Icons.MODEL_TRAINING,
                    on_click=lambda e, name=model_name, info=update_info: self._download_model_update(name, info, status_text, progress_bar)
                )
                update_buttons.append(model_btn)
        
        # 全部更新按钮
        if len(update_buttons) > 1:
            all_btn = ft.ElevatedButton(
                "全部更新",
                icon=ft.Icons.UPDATE,
                on_click=lambda e: self._download_all_updates(app_update, model_updates, status_text, progress_bar)
            )
            update_buttons.insert(0, all_btn)
        
        # 更新对话框内容
        if hasattr(self, '_update_dialog'):
            self._update_dialog.content.content.controls = [
                self._update_dialog.content.content.controls[0],  # 状态显示区域
                ft.Divider(),
                ft.Column(update_buttons, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ]
            self._update_dialog.content.content.update()
    
    def _download_app_update(self, app_update, status_text, progress_bar):
        """下载应用更新"""
        def progress_callback(url, progress, downloaded, total):
            status_text.value = f"下载应用更新: {progress:.1f}%"
            progress_bar.value = progress / 100
            progress_bar.visible = True
            progress_bar.update()
            status_text.update()
        
        def error_callback(error):
            status_text.value = f"应用更新失败: {error}"
            status_text.color = ft.Colors.RED
            status_text.update()
        
        def success_callback():
            status_text.value = "应用更新完成，请重启应用"
            status_text.color = ft.Colors.GREEN
            status_text.update()
        
        # 创建备份
        if update_manager.update_config.get("backup_before_update"):
            status_text.value = "正在创建备份..."
            status_text.update()
            update_manager.create_backup()
        
        # 开始下载
        status_text.value = "开始下载应用更新..."
        status_text.update()
        
        update_manager.download_app_update(
            app_update["update_url"],
            progress_callback=progress_callback,
            error_callback=error_callback
        )
    
    def _download_model_update(self, model_name, update_info, status_text, progress_bar):
        """下载模型更新"""
        def progress_callback(url, progress, downloaded, total):
            status_text.value = f"下载模型 {model_name}: {progress:.1f}%"
            progress_bar.value = progress / 100
            progress_bar.visible = True
            progress_bar.update()
            status_text.update()
        
        def error_callback(error):
            status_text.value = f"模型更新失败: {error}"
            status_text.color = ft.Colors.RED
            status_text.update()
        
        # 开始下载
        status_text.value = f"开始下载模型 {model_name}..."
        status_text.update()
        
        update_manager.download_model_update(
            model_name,
            update_info["url"],
            progress_callback=progress_callback,
            error_callback=error_callback
        )
    
    def _download_all_updates(self, app_update, model_updates, status_text, progress_bar):
        """下载所有更新"""
        def download_all():
            try:
                # 先下载应用更新
                if app_update and app_update.get("has_update"):
                    self._download_app_update(app_update, status_text, progress_bar)
                    # 等待应用更新完成
                    import time
                    time.sleep(2)
                
                # 再下载模型更新
                for model_name, update_info in model_updates.items():
                    if update_info.get("has_update"):
                        self._download_model_update(model_name, update_info, status_text, progress_bar)
                        time.sleep(1)
                
                status_text.value = "所有更新完成"
                status_text.color = ft.Colors.GREEN
                status_text.update()
                
            except Exception as e:
                status_text.value = f"批量更新失败: {str(e)}"
                status_text.color = ft.Colors.RED
                status_text.update()
        
        # 在后台线程中执行
        thread = threading.Thread(target=download_all, daemon=True)
        thread.start()