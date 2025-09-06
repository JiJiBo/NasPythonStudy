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
                subtitle=ft.Text("选择默认的大模型和参数配置", size=12, color=ft.Colors.GREY),
                on_click=lambda e: llm_setting_page(self.p, on_back=self.on_back),
            ),
            # 聊天记录历史条数设置
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HISTORY, size=30),
                title=ft.Text("聊天记录条数", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("聊天会加载几条历史记录，当作记忆？", size=12, color=ft.Colors.GREY),
                on_click=self._open_history_setting,
            ),
            # 系统信息
            ft.ListTile(
                leading=ft.Icon(ft.Icons.INFO, size=30),
                title=ft.Text("系统信息", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("查看CUDA版本、GPU信息等", size=12, color=ft.Colors.GREY),
                on_click=self._open_system_info_dialog,
            ),
            # PyTorch版本选择器
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SELECT_ALL, size=30),
                title=ft.Text("PyTorch版本选择器", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("智能推荐适合您显卡的PyTorch版本", size=12, color=ft.Colors.GREY),
                on_click=self._open_torch_selector,
            ),
            # PyTorch拖拽安装器
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CLOUD_UPLOAD, size=30),
                title=ft.Text("PyTorch拖拽安装器", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("从官网下载.whl文件，拖拽安装", size=12, color=ft.Colors.GREY),
                on_click=self._open_drag_installer,
            ),
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
            height=400,
            width=500,
            padding=15,
            bgcolor=ft.Colors.GREY_50,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_300),
            alignment=ft.alignment.center
        )
        
        # 创建信息显示文本（初始为空）
        info_text = ft.Text(
            "",
            size=12,
            selectable=True,
            font_family="Consolas, monospace"
        )
        
        # 创建滚动容器
        info_container = ft.Container(
            content=info_text,
            height=400,
            width=500,
            padding=15,
            bgcolor=ft.Colors.GREY_50,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_300),
            visible=False  # 初始隐藏，等待加载完成后显示
        )
        
        # 创建刷新按钮
        refresh_btn = ft.ElevatedButton(
            "刷新信息",
            on_click=lambda e: self._refresh_system_info_with_loading(info_text, info_container, loading_container, loading_text, loading_progress)
        )
        
        # 创建关闭按钮
        close_btn = ft.TextButton(
            "关闭",
            on_click=lambda e: self.p.close(self.system_info_dialog)
        )
        
        # 按钮行
        button_row = ft.Row([refresh_btn, close_btn], alignment=ft.MainAxisAlignment.END)
        
        # 创建对话框
        self.system_info_dialog = ft.AlertDialog(
            title=ft.Text("系统信息"),
            content=ft.Column([
                ft.Text("当前系统配置信息：", size=14, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                loading_container,  # 初始显示加载状态
                info_container,     # 信息显示容器（初始隐藏）
                button_row
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            modal=True,
            actions_padding=0
        )
        
        self.p.dialog = self.system_info_dialog
        self.p.open(self.system_info_dialog)
        self.p.update()
        
        # 在后台线程中加载系统信息
        threading.Thread(target=self._load_system_info_async, 
                        args=(info_text, info_container, loading_container, loading_text, loading_progress), 
                        daemon=True).start()

    def _load_system_info_async(self, info_text, info_container, loading_container, loading_text, loading_progress):
        """异步加载系统信息"""
        try:
            print("开始异步加载系统信息...")
            
            # 更新加载状态
            def update_loading_status(message):
                print(f"更新加载状态: {message}")
                loading_text.value = message
                self.p.update()
            
            self.p.run_thread(lambda: update_loading_status("正在检测CUDA版本..."))
            
            # 获取系统信息
            print("正在获取系统信息...")
            from src.utils.SystemInfo import format_system_info
            formatted_info = format_system_info()
            print(f"系统信息获取完成，长度: {len(formatted_info)}")
            
            # 更新UI显示结果
            def show_result():
                print("显示系统信息结果...")
                info_text.value = formatted_info
                # 隐藏加载状态，显示结果
                loading_container.visible = False
                info_container.visible = True
                self.p.update()
                print("系统信息显示完成")
            
            self.p.run_thread(show_result)
            
        except Exception as e:
            print(f"异步加载系统信息出错: {e}")
            import traceback
            traceback.print_exc()
            
            # 显示错误信息
            def show_error():
                error_msg = f"获取系统信息失败: {str(e)}"
                print(f"显示错误信息: {error_msg}")
                info_text.value = error_msg
                loading_container.visible = False
                info_container.visible = True
                self.p.update()
            
            self.p.run_thread(show_error)

    def _refresh_system_info_with_loading(self, info_text, info_container, loading_container, loading_text, loading_progress):
        """带加载状态的刷新系统信息"""
        # 显示加载状态
        loading_container.visible = True
        info_container.visible = False
        loading_text.value = "正在刷新系统信息..."
        self.p.update()
        
        # 清除缓存并重新加载
        from src.utils.SystemInfo import clear_system_info_cache
        clear_system_info_cache()
        
        # 在后台线程中重新加载
        threading.Thread(target=self._load_system_info_async, 
                        args=(info_text, info_container, loading_container, loading_text, loading_progress), 
                        daemon=True).start()

    def _refresh_system_info(self, info_text, info_container):
        """刷新系统信息（保持向后兼容）"""
        try:
            # 重新获取系统信息
            formatted_info = format_system_info()
            info_text.value = formatted_info
            self.p.update()
        except Exception as e:
            info_text.value = f"获取系统信息失败: {str(e)}"
            self.p.update()


    def _open_torch_selector(self, e):
        """打开PyTorch版本选择器"""
        try:
            # 获取项目根目录 - 从src/ui/home/向上3级到项目根目录
            current_dir = os.path.dirname(__file__)  # src/ui/home/
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # 项目根目录
            script_path = os.path.join(project_root, "python_env", "launch_torch_selector.py")
            script_path = os.path.abspath(script_path)
            
            print(f"当前文件目录: {current_dir}")
            print(f"项目根目录: {project_root}")
            print(f"脚本路径: {script_path}")
            print(f"脚本是否存在: {os.path.exists(script_path)}")
            
            if not os.path.exists(script_path):
                # 显示错误对话框
                error_dialog = ft.AlertDialog(
                    title=ft.Text("错误"),
                    content=ft.Text(f"PyTorch版本选择器脚本不存在\n路径: {script_path}"),
                    actions=[ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))]
                )
                self.p.dialog = error_dialog
                self.p.open(error_dialog)
                return
            
            # 显示启动对话框
            start_dialog = ft.AlertDialog(
                title=ft.Text("启动PyTorch版本选择器"),
                content=ft.Column([
                    ft.Text("将启动智能PyTorch版本选择器，系统会："),
                    ft.Text("• 自动检测您的显卡和驱动信息", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• 智能推荐最适合的CUDA版本", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• 显示详细的下载地址和兼容性信息", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• 支持一键安装推荐版本", size=12, color=ft.Colors.GREY_600),
                    ft.Divider(),
                    ft.Text("可用版本：", weight=ft.FontWeight.BOLD),
                    ft.Text("• CUDA 11.8 ", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• CUDA 12.1 ", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• CUDA 12.4 ", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• CUDA 12.6 ", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• CUDA 12.8 ", size=12, color=ft.Colors.GREY_600),
                    ft.Text("• CPU版本", size=12, color=ft.Colors.GREY_600),
                ], tight=True),
                actions=[
                    ft.TextButton("启动", on_click=lambda e: self._start_torch_selector(script_path, start_dialog)),
                    ft.TextButton("取消", on_click=lambda e: self.p.close(start_dialog))
                ]
            )
            self.p.dialog = start_dialog
            self.p.open(start_dialog)
            
        except Exception as ex:
            error_dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.Text(f"启动PyTorch版本选择器失败: {str(ex)}"),
                actions=[ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))]
            )
            self.p.dialog = error_dialog
            self.p.open(error_dialog)

    def _start_torch_selector(self, script_path, dialog):
        """启动PyTorch版本选择器"""
        try:
            # 关闭对话框
            self.p.close(dialog)
            
            # 在后台启动PyTorch选择器
            import subprocess
            subprocess.Popen([sys.executable, script_path])
            
        except Exception as e:
            error_dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.Text(f"启动失败: {str(e)}"),
                actions=[ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))]
            )
            self.p.dialog = error_dialog
            self.p.open(error_dialog)

    def _open_drag_installer(self, e):
        """打开PyTorch拖拽安装器"""
        try:
            # 获取拖拽安装器脚本路径
            current_dir = os.path.dirname(__file__)  # src/ui/home/
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # 项目根目录
            script_path = os.path.join(project_root, "python_env", "launch_drag_installer.py")
            script_path = os.path.abspath(script_path)
            
            print(f"拖拽安装器脚本路径: {script_path}")
            print(f"脚本是否存在: {os.path.exists(script_path)}")
            
            if not os.path.exists(script_path):
                # 显示错误对话框
                error_dialog = ft.AlertDialog(
                    title=ft.Text("错误"),
                    content=ft.Text(f"PyTorch拖拽安装器脚本不存在\n路径: {script_path}"),
                    actions=[ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))]
                )
                self.p.dialog = error_dialog
                self.p.open(error_dialog)
                return
            
            # 显示启动对话框
            start_dialog = ft.AlertDialog(
                title=ft.Text("启动PyTorch拖拽安装器"),
                content=ft.Column([
                    ft.Text("将启动PyTorch拖拽安装器，您可以："),
                    ft.Text("1. 从PyTorch官网下载.whl文件", size=12, color=ft.Colors.GREY_600),
                    ft.Text("2. 拖拽文件到安装器界面", size=12, color=ft.Colors.GREY_600),
                    ft.Text("3. 自动安装对应的CUDA版本", size=12, color=ft.Colors.GREY_600),
                    ft.Divider(),
                    ft.Text("推荐下载链接：", weight=ft.FontWeight.BOLD),
                    ft.Text("• CUDA 12.4 : https://download.pytorch.org/whl/cu124", size=10, color=ft.Colors.BLUE),
                    ft.Text("• CUDA 12.1 : https://download.pytorch.org/whl/cu121", size=10, color=ft.Colors.BLUE),
                    ft.Text("• CUDA 12.8 : https://download.pytorch.org/whl/cu128", size=10, color=ft.Colors.BLUE),
                ], tight=True),
                actions=[
                    ft.TextButton("启动", on_click=lambda e: self._start_drag_installer(script_path, start_dialog)),
                    ft.TextButton("取消", on_click=lambda e: self.p.close(start_dialog))
                ]
            )
            self.p.dialog = start_dialog
            self.p.open(start_dialog)
            
        except Exception as ex:
            error_dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.Text(f"启动PyTorch拖拽安装器失败: {str(ex)}"),
                actions=[ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))]
            )
            self.p.dialog = error_dialog
            self.p.open(error_dialog)

    def _start_drag_installer(self, script_path, dialog):
        """启动PyTorch拖拽安装器"""
        try:
            # 关闭对话框
            self.p.close(dialog)
            
            # 在后台启动拖拽安装器
            import subprocess
            subprocess.Popen([sys.executable, script_path])
            
        except Exception as e:
            error_dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.Text(f"启动失败: {str(e)}"),
                actions=[ft.TextButton("确定", on_click=lambda e: self.p.close(error_dialog))]
            )
            self.p.dialog = error_dialog
            self.p.open(error_dialog)
