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
            # 一键安装环境
            ft.ListTile(
                leading=ft.Icon(ft.Icons.DOWNLOAD, size=30),
                title=ft.Text("一键安装环境", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("自动安装本地模型所需的依赖包", size=12, color=ft.Colors.GREY),
                on_click=self._open_install_dialog,
            ),
            # 系统信息
            ft.ListTile(
                leading=ft.Icon(ft.Icons.INFO, size=30),
                title=ft.Text("系统信息", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("查看CUDA版本、GPU信息等", size=12, color=ft.Colors.GREY),
                on_click=self._open_system_info_dialog,
            ),
            # 重新安装CUDA torch
            ft.ListTile(
                leading=ft.Icon(ft.Icons.REFRESH, size=30),
                title=ft.Text("重新安装CUDA torch", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("重新安装CUDA版本的PyTorch", size=12, color=ft.Colors.GREY),
                on_click=self._open_reinstall_cuda_dialog,
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

    def _open_install_dialog(self, e):
        """打开安装环境对话框"""
        # 创建进度显示组件
        self.progress_bar = ft.ProgressBar(width=300, visible=False)
        self.status_text = ft.Text("准备安装...", size=14)
        self.log_text = ft.Text("", size=12, color=ft.Colors.GREY_600, selectable=True)
        
        # 创建滚动容器显示日志
        self.log_container = ft.Container(
            content=self.log_text,
            height=200,
            width=400,
            padding=10,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
            visible=False
        )
        
        # 安装按钮
        self.install_btn = ft.ElevatedButton(
            "开始安装",
            on_click=self._start_install,
            disabled=False
        )
        
        # 关闭按钮
        self.close_btn = ft.TextButton(
            "关闭",
            on_click=lambda e: self.p.close(self.install_dialog)
        )
        
        # 按钮行
        self.button_row = ft.Row([self.install_btn, self.close_btn], alignment=ft.MainAxisAlignment.END)
        
        # 创建对话框
        self.install_dialog = ft.AlertDialog(
            title=ft.Text("一键安装环境"),
            content=ft.Column([
                ft.Text("将自动安装本地模型所需的依赖包：", size=14),
                ft.Text("• torch (根据显卡自动选择版本)", size=12, color=ft.Colors.GREY_600),
                ft.Text("• transformers (模型推理库)", size=12, color=ft.Colors.GREY_600),
                ft.Text("• requests, tqdm (基础依赖)", size=12, color=ft.Colors.GREY_600),
                ft.Divider(),
                self.status_text,
                self.progress_bar,
                self.log_container,
                self.button_row
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            modal=True,
            actions_padding=0
        )
        
        self.p.dialog = self.install_dialog
        self.p.open(self.install_dialog)
        self.p.update()

    def _start_install(self, e):
        """开始安装依赖"""
        self.install_btn.disabled = True
        self.install_btn.text = "安装中..."
        self.progress_bar.visible = True
        self.log_container.visible = True
        self.status_text.value = "正在安装依赖包..."
        self.p.update()
        
        # 在后台线程中运行安装
        threading.Thread(target=self._run_install, daemon=True).start()

    def _run_install(self):
        """在后台线程中运行安装"""
        try:
            # 获取安装脚本路径
            script_path = os.path.join(os.path.dirname(__file__), "..", "..", "utils", "install_dependencies.py")
            script_path = os.path.abspath(script_path)
            
            self._update_log("开始安装依赖包...")
            self._update_log(f"脚本路径: {script_path}")
            
            # 运行安装脚本
            # 设置环境变量确保UTF-8编码
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',  # 使用replace而不是ignore，避免丢失字符
                bufsize=1,
                universal_newlines=True,
                env=env
            )
            
            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    # 处理编码问题，确保正确显示中文
                    try:
                        # 如果line已经是字符串，直接使用
                        clean_line = line.strip()
                    except UnicodeDecodeError:
                        # 如果出现编码错误，尝试重新解码
                        clean_line = line.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore').strip()
                    
                    if clean_line:
                        self._update_log(clean_line)
            
            # 等待进程完成
            return_code = process.wait()
            
            if return_code == 0:
                self._update_status("安装完成！", ft.Colors.GREEN)
                self._update_log("✅ 所有依赖安装成功！")
            else:
                self._update_status("安装失败", ft.Colors.RED)
                self._update_log("❌ 安装过程中出现错误")
                
        except Exception as e:
            self._update_status("安装出错", ft.Colors.RED)
            self._update_log(f"❌ 错误: {str(e)}")
        finally:
            # 恢复按钮状态
            self.install_btn.disabled = False
            self.install_btn.text = "重新安装"
            self.progress_bar.visible = False
            self.p.update()

    def _update_log(self, message):
        """更新日志显示"""
        def update():
            current_log = self.log_text.value
            if current_log:
                self.log_text.value = current_log + "\n" + message
            else:
                self.log_text.value = message
            self.p.update()
        
        # 在主线程中更新UI
        self.p.run_thread(update)

    def _update_status(self, message, color=ft.Colors.BLACK):
        """更新状态显示"""
        def update():
            self.status_text.value = message
            self.status_text.color = color
            self.p.update()
        
        # 在主线程中更新UI
        self.p.run_thread(update)

    def _open_system_info_dialog(self, e):
        """打开系统信息对话框"""
        # 获取系统信息
        system_info = get_system_info()
        formatted_info = format_system_info()
        
        # 创建信息显示文本
        info_text = ft.Text(
            formatted_info,
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
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        # 创建刷新按钮
        refresh_btn = ft.ElevatedButton(
            "刷新信息",
            on_click=lambda e: self._refresh_system_info(info_text, info_container)
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
                info_container,
                button_row
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            modal=True,
            actions_padding=0
        )
        
        self.p.dialog = self.system_info_dialog
        self.p.open(self.system_info_dialog)
        self.p.update()

    def _refresh_system_info(self, info_text, info_container):
        """刷新系统信息"""
        try:
            # 重新获取系统信息
            formatted_info = format_system_info()
            info_text.value = formatted_info
            self.p.update()
        except Exception as e:
            info_text.value = f"获取系统信息失败: {str(e)}"
            self.p.update()

    def _open_reinstall_cuda_dialog(self, e):
        """打开重新安装CUDA torch对话框"""
        # 创建进度显示组件
        self.cuda_progress_bar = ft.ProgressBar(width=300, visible=False)
        self.cuda_status_text = ft.Text("准备重新安装CUDA版本的torch...", size=14)
        self.cuda_log_text = ft.Text("", size=12, color=ft.Colors.GREY_600, selectable=True)
        
        # 创建滚动容器显示日志
        self.cuda_log_container = ft.Container(
            content=self.cuda_log_text,
            height=200,
            width=400,
            padding=10,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
            visible=False
        )
        
        # 重新安装按钮
        self.reinstall_cuda_btn = ft.ElevatedButton(
            "开始重新安装",
            on_click=self._start_reinstall_cuda,
            disabled=False
        )
        
        # 关闭按钮
        self.cuda_close_btn = ft.TextButton(
            "关闭",
            on_click=lambda e: self.p.close(self.reinstall_cuda_dialog)
        )
        
        # 按钮行
        self.cuda_button_row = ft.Row([self.reinstall_cuda_btn, self.cuda_close_btn], alignment=ft.MainAxisAlignment.END)
        
        # 创建对话框
        self.reinstall_cuda_dialog = ft.AlertDialog(
            title=ft.Text("重新安装CUDA torch"),
            content=ft.Column([
                ft.Text("将重新安装CUDA版本的PyTorch：", size=14),
                ft.Text("• 自动检测CUDA版本", size=12, color=ft.Colors.GREY_600),
                ft.Text("• 卸载现有torch版本", size=12, color=ft.Colors.GREY_600),
                ft.Text("• 安装匹配的CUDA版本", size=12, color=ft.Colors.GREY_600),
                ft.Text("• 验证GPU可用性", size=12, color=ft.Colors.GREY_600),
                ft.Divider(),
                self.cuda_status_text,
                self.cuda_progress_bar,
                self.cuda_log_container,
                self.cuda_button_row
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            modal=True,
            actions_padding=0
        )
        
        self.p.dialog = self.reinstall_cuda_dialog
        self.p.open(self.reinstall_cuda_dialog)
        self.p.update()

    def _start_reinstall_cuda(self, e):
        """开始重新安装CUDA torch"""
        self.reinstall_cuda_btn.disabled = True
        self.reinstall_cuda_btn.text = "安装中..."
        self.cuda_progress_bar.visible = True
        self.cuda_log_container.visible = True
        self.cuda_status_text.value = "正在重新安装CUDA版本的torch..."
        self.p.update()
        
        # 在后台线程中运行安装
        threading.Thread(target=self._run_reinstall_cuda, daemon=True).start()

    def _run_reinstall_cuda(self):
        """在后台线程中运行重新安装CUDA torch"""
        try:
            # 获取安装脚本路径
            script_path = os.path.join(os.path.dirname(__file__), "..", "..", "utils", "install_dependencies.py")
            script_path = os.path.abspath(script_path)
            
            self._update_cuda_log("开始重新安装CUDA版本的torch...")
            self._update_cuda_log(f"脚本路径: {script_path}")
            
            # 设置环境变量确保UTF-8编码
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # 运行安装脚本，使用--reinstall-cuda参数
            process = subprocess.Popen(
                [sys.executable, script_path, "--reinstall-cuda"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                universal_newlines=True,
                env=env
            )
            
            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    # 处理编码问题，确保正确显示中文
                    try:
                        clean_line = line.strip()
                    except UnicodeDecodeError:
                        clean_line = line.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore').strip()
                    
                    if clean_line:
                        self._update_cuda_log(clean_line)
            
            # 等待进程完成
            return_code = process.wait()
            
            if return_code == 0:
                self._update_cuda_status("重新安装完成！", ft.Colors.GREEN)
                self._update_cuda_log("✅ CUDA版本torch重新安装成功！")
            else:
                self._update_cuda_status("重新安装失败", ft.Colors.RED)
                self._update_cuda_log("❌ 重新安装过程中出现错误")
                
        except Exception as e:
            self._update_cuda_status("重新安装出错", ft.Colors.RED)
            self._update_cuda_log(f"❌ 错误: {str(e)}")
        finally:
            # 恢复按钮状态
            self.reinstall_cuda_btn.disabled = False
            self.reinstall_cuda_btn.text = "重新安装"
            self.cuda_progress_bar.visible = False
            self.p.update()

    def _update_cuda_log(self, message):
        """更新CUDA安装日志显示"""
        def update():
            current_log = self.cuda_log_text.value
            if current_log:
                self.cuda_log_text.value = current_log + "\n" + message
            else:
                self.cuda_log_text.value = message
            self.p.update()
        
        # 在主线程中更新UI
        self.p.run_thread(update)

    def _update_cuda_status(self, message, color=ft.Colors.BLACK):
        """更新CUDA安装状态显示"""
        def update():
            self.cuda_status_text.value = message
            self.cuda_status_text.color = color
            self.p.update()
        
        # 在主线程中更新UI
        self.p.run_thread(update)
