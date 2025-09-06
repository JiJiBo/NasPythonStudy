#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyTorch拖拽安装器
用户从官网下载CUDA版本的torch文件，拖拽到应用中进行安装
"""

import flet as ft
import subprocess
import sys
import os
import threading
from pathlib import Path
import zipfile
import tempfile
import shutil

class TorchDragInstaller:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PyTorch拖拽安装器"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 900
        self.page.window_height = 800
        self.page.window_resizable = True
        
        # 获取系统信息
        self.system_info = self.get_system_info()
        
        # 支持的PyTorch版本信息（根据系统配置动态生成）
        self.torch_versions = self.generate_torch_versions()
        
        self.dropped_files = []
        self.install_progress = None
        self.install_status = None
        self.install_log = None
        
        self.build_ui()
    
    def get_system_info(self):
        """获取系统信息"""
        import platform
        import subprocess
        
        info = {
            "python_version": platform.python_version(),
            "python_major_minor": f"{platform.python_version_tuple()[0]}.{platform.python_version_tuple()[1]}",
            "architecture": platform.machine(),
            "system": platform.system(),
            "processor": platform.processor()
        }
        
        # 获取CUDA版本
        try:
            result = subprocess.run(["nvidia-smi", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "CUDA Version" in line:
                        cuda_version = line.split("CUDA Version")[-1].strip()
                        info["cuda_version"] = cuda_version
                        break
        except:
            info["cuda_version"] = "未检测到"
        
        # 获取GPU信息
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                gpu_info = result.stdout.strip().split('\n')[0]
                info["gpu_info"] = gpu_info
            else:
                info["gpu_info"] = "未检测到GPU"
        except:
            info["gpu_info"] = "未检测到GPU"
        
        return info
    
    def generate_torch_versions(self):
        """根据系统配置生成PyTorch版本信息"""
        python_version = self.system_info["python_major_minor"]
        architecture = self.system_info["architecture"]
        system = self.system_info["system"]
        
        # 根据系统确定文件后缀
        if system == "Windows":
            if architecture == "AMD64":
                platform_suffix = "win_amd64"
            else:
                platform_suffix = "win_32"
        elif system == "Linux":
            platform_suffix = "linux_x86_64"
        elif system == "Darwin":  # macOS
            platform_suffix = "macosx_10_9_x86_64"
        else:
            platform_suffix = "linux_x86_64"  # 默认
        
        # 根据Python版本确定cp标签
        python_cp = f"cp{python_version.replace('.', '')}"
        
        # 最新版本配置（基于PyTorch官网最新版本）
        versions = {
            "CUDA 11.8": {
                "description": "RTX 30系列显卡，稳定版本",
                "download_url": "https://download.pytorch.org/whl/cu118",
                "files": [
                    {
                        "name": f"torch-2.5.1+cu118-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu118/torch-2.5.1+cu118-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchvision-0.20.1+cu118-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu118/torchvision-0.20.1+cu118-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchaudio-2.5.1+cu118-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu118/torchaudio-2.5.1+cu118-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    }
                ],
                "min_driver": "470.0",
                "compatible_gpus": ["RTX 30", "GTX 16", "GTX 10"]
            },
            "CUDA 12.1": {
                "description": "RTX 40系列显卡，通用版本",
                "download_url": "https://download.pytorch.org/whl/cu121",
                "files": [
                    {
                        "name": f"torch-2.5.1+cu121-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu121/torch-2.5.1+cu121-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchvision-0.20.1+cu121-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu121/torchvision-0.20.1+cu121-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchaudio-2.5.1+cu121-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu121/torchaudio-2.5.1+cu121-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    }
                ],
                "min_driver": "525.0",
                "compatible_gpus": ["RTX 40", "RTX 30", "GTX 16"]
            },
            "CUDA 12.4": {
                "description": "RTX 50系和40系显卡，通用版本",
                "download_url": "https://download.pytorch.org/whl/cu124",
                "files": [
                    {
                        "name": f"torch-2.5.1+cu124-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu124/torch-2.5.1+cu124-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchvision-0.20.1+cu124-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu124/torchvision-0.20.1+cu124-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchaudio-2.5.1+cu124-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu124/torchaudio-2.5.1+cu124-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    }
                ],
                "min_driver": "550.0",
                "compatible_gpus": ["RTX 50", "RTX 40", "RTX 30"]
            },
            "CUDA 12.6": {
                "description": "RTX 50系和40系显卡，稳定版本",
                "download_url": "https://download.pytorch.org/whl/cu126",
                "files": [
                    {
                        "name": f"torch-2.5.1+cu126-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu126/torch-2.5.1+cu126-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchvision-0.20.1+cu126-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu126/torchvision-0.20.1+cu126-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchaudio-2.5.1+cu126-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu126/torchaudio-2.5.1+cu126-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    }
                ],
                "min_driver": "555.0",
                "compatible_gpus": ["RTX 50", "RTX 40", "RTX 30"]
            },
            "CUDA 12.8": {
                "description": "RTX 50系列显卡，最新版本",
                "download_url": "https://download.pytorch.org/whl/cu128",
                "files": [
                    {
                        "name": f"torch-2.8.0+cu128-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu128/torch-2.8.0+cu128-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchvision-0.23.0+cu128-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu128/torchvision-0.23.0+cu128-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchaudio-2.8.0+cu128-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cu128/torchaudio-2.8.0+cu128-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    }
                ],
                "min_driver": "560.0",
                "compatible_gpus": ["RTX 50", "RTX 40"]
            },
            "CPU版本": {
                "description": "无GPU或CPU训练，通用版本",
                "download_url": "https://download.pytorch.org/whl/cpu",
                "files": [
                    {
                        "name": f"torch-2.5.1+cpu-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cpu/torch-2.5.1+cpu-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchvision-0.20.1+cpu-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cpu/torchvision-0.20.1+cpu-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    },
                    {
                        "name": f"torchaudio-2.5.1+cpu-{python_cp}-{python_cp}-{platform_suffix}.whl",
                        "url": f"https://download.pytorch.org/whl/cpu/torchaudio-2.5.1+cpu-{python_cp}-{python_cp}-{platform_suffix}.whl"
                    }
                ],
                "min_driver": "N/A",
                "compatible_gpus": ["所有CPU"]
            }
        }
        
        return versions
    
    def build_ui(self):
        """构建用户界面"""
        # 标题
        title = ft.Text(
            "PyTorch拖拽安装器",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        # 说明文本
        instruction = ft.Text(
            "从PyTorch官网下载CUDA版本的.whl文件，然后拖拽到下方区域进行安装",
            size=14,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER
        )
        
        # 下载指导
        download_guide = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📥 下载指导", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("1. 点击下方'打开PyTorch官网'按钮", size=12),
                    ft.Text("2. 在官网页面中找到对应的文件名", size=12),
                    ft.Text("3. 点击文件名进行下载", size=12),
                    ft.Text("4. 将下载的.whl文件拖拽到下方区域", size=12),
                    ft.ElevatedButton(
                        "🌐 打开PyTorch官网",
                        on_click=self.open_pytorch_website,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.ORANGE,
                            color=ft.Colors.WHITE
                        )
                    )
                ], spacing=8),
                padding=15
            ),
            color=ft.Colors.ORANGE_100
        )
        
        # 系统信息卡片
        system_info_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("系统信息", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Python版本: {self.system_info['python_version']}", size=12),
                    ft.Text(f"系统架构: {self.system_info['architecture']}", size=12),
                    ft.Text(f"操作系统: {self.system_info['system']}", size=12),
                    ft.Text(f"CUDA版本: {self.system_info['cuda_version']}", size=12),
                    ft.Text(f"GPU信息: {self.system_info['gpu_info']}", size=12),
                ], spacing=5),
                padding=15
            )
        )
        
        # 版本信息表格
        version_table = self.create_version_table()
        
        # 拖拽区域
        drop_area = self.create_drop_area()
        
        # 已选择文件列表
        self.file_list = ft.Column(spacing=5)
        
        # 安装按钮
        self.install_btn = ft.ElevatedButton(
            "开始安装",
            on_click=self.start_install,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE
            )
        )
        
        # 进度条
        self.install_progress = ft.ProgressBar(
            width=600,
            visible=False
        )
        
        # 状态文本
        self.install_status = ft.Text(
            "请拖拽PyTorch的.whl文件到上方区域",
            size=14,
            text_align=ft.TextAlign.CENTER
        )
        
        # 日志显示
        self.install_log = ft.Text(
            "",
            size=12,
            color=ft.Colors.GREY_600,
            selectable=True
        )
        
        self.log_container = ft.Container(
            content=self.install_log,
            height=200,
            width=800,
            padding=10,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
            visible=False
        )
        
        # 主布局
        main_column = ft.Column([
            title,
            instruction,
            ft.Divider(),
            download_guide,
            ft.Divider(),
            system_info_card,
            ft.Divider(),
            ft.Text("支持的PyTorch版本:", size=16, weight=ft.FontWeight.BOLD),
            version_table,
            ft.Divider(),
            ft.Text("拖拽区域:", size=16, weight=ft.FontWeight.BOLD),
            drop_area,
            ft.Text("已选择的文件:", size=14, weight=ft.FontWeight.BOLD),
            self.file_list,
            ft.Divider(),
            self.install_btn,
            self.install_progress,
            self.install_status,
            self.log_container
        ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        
        # 使用可滚动的容器包装主布局
        scrollable_container = ft.Container(
            content=main_column,
            expand=True,
            padding=20
        )
        
        self.page.add(scrollable_container)
    
    def create_version_table(self):
        """创建版本信息表格"""
        table_rows = []

        
        # 数据行
        for version, info in self.torch_versions.items():
            # 显示文件名（只显示第一个作为示例）
            sample_file = info["files"][0]["name"] if info["files"] else "N/A"
            
            # 创建文件下载按钮
            file_buttons = ft.ElevatedButton(
                "复制文件名",
                on_click=lambda e, file_name=info["files"][0]["name"]: self.copy_file_name(file_name),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE
                ),
                width=100,
                height=30
            )
            
            data_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(version, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(info["description"], size=11)),
                    ft.DataCell(ft.Text(f"最低驱动: {info['min_driver']}", size=10)),
                    ft.DataCell(ft.Text(f"兼容GPU: {', '.join(info['compatible_gpus'])}", size=10)),
                    ft.DataCell(ft.Text(sample_file, size=9, color=ft.Colors.GREY_600)),
                    ft.DataCell(file_buttons)
                ]
            )
            table_rows.append(data_row)
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CUDA版本")),
                ft.DataColumn(ft.Text("适用显卡")),
                ft.DataColumn(ft.Text("最低驱动")),
                ft.DataColumn(ft.Text("兼容GPU")),
                ft.DataColumn(ft.Text("示例文件名")),
                ft.DataColumn(ft.Text("操作"))
            ],
            rows=table_rows,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8
        )
    
    def create_drop_area(self):
        """创建拖拽区域"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CLOUD_UPLOAD, size=48, color=ft.Colors.BLUE),
                ft.Text("拖拽.whl文件到这里", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("支持torch、torchvision、torchaudio文件", size=12, color=ft.Colors.GREY_600)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=800,
            height=150,
            border=ft.border.all(2, ft.Colors.BLUE),
            border_radius=8,
            bgcolor=ft.Colors.BLUE_50,
            alignment=ft.alignment.center,
            on_click=self.open_file_dialog
        )
    
    def copy_url(self, url):
        """复制URL到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(url)
            self.update_status("链接已复制到剪贴板！", ft.Colors.GREEN)
        except ImportError:
            # 如果没有pyperclip，显示URL
            self.update_status(f"请手动复制链接: {url}", ft.Colors.ORANGE)
    
    def copy_file_name(self, file_name):
        """复制文件名到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(file_name)
            self.update_status("文件名已复制到剪贴板！", ft.Colors.GREEN)
        except ImportError:
            # 如果没有pyperclip，显示文件名
            self.update_status(f"请手动复制文件名: {file_name}", ft.Colors.ORANGE)
    
    
    def open_pytorch_website(self, e):
        """打开PyTorch官网"""
        import webbrowser
        webbrowser.open("https://download.pytorch.org/whl/torch/")
        self.update_status("已打开PyTorch官网，请查找对应的文件名进行下载", ft.Colors.BLUE)
    
    def open_file_dialog(self, e):
        """打开文件选择对话框"""
        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                for file in e.files:
                    self.add_file(file.path)
        
        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        file_picker.pick_files(
            dialog_title="选择PyTorch .whl文件",
            allowed_extensions=["whl"],
            allow_multiple=True
        )
    
    def add_file(self, file_path):
        """添加文件到列表"""
        file_name = os.path.basename(file_path)
        
        # 检查是否是PyTorch相关文件
        if not any(keyword in file_name.lower() for keyword in ['torch', 'torchvision', 'torchaudio']):
            self.update_status(f"警告: {file_name} 不是PyTorch相关文件", ft.Colors.ORANGE)
            return
        
        # 检查是否已存在
        if file_path in self.dropped_files:
            self.update_status(f"文件 {file_name} 已存在", ft.Colors.ORANGE)
            return
        
        self.dropped_files.append(file_path)
        
        # 添加到UI列表
        file_item = ft.Row([
            ft.Icon(ft.Icons.INSERT_DRIVE_FILE, color=ft.Colors.BLUE),
            ft.Text(file_name, expand=True),
            ft.IconButton(
                ft.Icons.DELETE,
                on_click=lambda e, path=file_path: self.remove_file(path),
                tooltip="删除文件"
            )
        ])
        
        self.file_list.controls.append(file_item)
        
        # 更新安装按钮状态
        self.install_btn.disabled = len(self.dropped_files) == 0
        self.update_status(f"已添加 {len(self.dropped_files)} 个文件", ft.Colors.BLUE)
        self.page.update()
    
    def remove_file(self, file_path):
        """从列表中移除文件"""
        if file_path in self.dropped_files:
            self.dropped_files.remove(file_path)
            
            # 从UI列表中移除
            for i, control in enumerate(self.file_list.controls):
                if hasattr(control, 'controls') and len(control.controls) > 2:
                    if control.controls[1].value == os.path.basename(file_path):
                        self.file_list.controls.pop(i)
                        break
            
            # 更新安装按钮状态
            self.install_btn.disabled = len(self.dropped_files) == 0
            self.update_status(f"已添加 {len(self.dropped_files)} 个文件", ft.Colors.BLUE)
            self.page.update()
    
    def start_install(self, e):
        """开始安装"""
        if not self.dropped_files:
            return
        
        # 更新UI状态
        self.install_btn.disabled = True
        self.install_btn.text = "安装中..."
        self.install_progress.visible = True
        self.install_status.value = "正在安装PyTorch..."
        self.install_status.color = ft.Colors.ORANGE
        
        # 显示日志容器
        self.log_container.visible = True
        
        self.page.update()
        
        # 在后台线程中执行安装
        threading.Thread(target=self.install_torch, daemon=True).start()
    
    def install_torch(self):
        """安装PyTorch"""
        try:
            python_exe = Path("python_env/python.exe")
            
            if not python_exe.exists():
                self.update_log("❌ Python可执行文件不存在")
                return
            
            self.update_log(f"开始安装 {len(self.dropped_files)} 个PyTorch文件...")
            self.update_log(f"使用Python: {python_exe}")
            
            # 卸载现有版本
            self.update_log("卸载现有PyTorch...")
            subprocess.run([
                str(python_exe), "-m", "pip", "uninstall", 
                "torch", "torchvision", "torchaudio", "-y"
            ], check=False)
            
            # 安装新版本
            self.update_log("安装新版本...")
            for i, file_path in enumerate(self.dropped_files):
                self.update_log(f"安装文件 {i+1}/{len(self.dropped_files)}: {os.path.basename(file_path)}")
                
                cmd = [str(python_exe), "-m", "pip", "install", file_path]
                self.update_log(f"执行命令: {' '.join(cmd)}")
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                # 实时读取输出
                for line in iter(process.stdout.readline, ''):
                    if line.strip():
                        self.update_log(line.strip())
                
                return_code = process.wait()
                
                if return_code == 0:
                    self.update_log(f"✅ {os.path.basename(file_path)} 安装成功")
                else:
                    self.update_log(f"❌ {os.path.basename(file_path)} 安装失败")
            
            # 验证安装
            self.verify_installation()
            
        except Exception as e:
            self.update_log(f"❌ 安装出错: {e}")
            self.install_status.value = f"❌ 安装出错: {e}"
            self.install_status.color = ft.Colors.RED
        finally:
            # 恢复按钮状态
            self.install_btn.disabled = False
            self.install_btn.text = "重新安装"
            self.install_progress.visible = False
            self.page.update()
    
    def verify_installation(self):
        """验证安装"""
        try:
            python_exe = Path("python_env/python.exe")
            result = subprocess.run([
                str(python_exe), "-c",
                "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU数量: {torch.cuda.device_count() if torch.cuda.is_available() else 0}')"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.update_log("✅ 验证结果:")
                self.update_log(result.stdout)
                self.install_status.value = "✅ PyTorch安装成功！"
                self.install_status.color = ft.Colors.GREEN
                
                # 安装成功后刷新系统信息
                self.update_log("🔄 正在刷新系统信息...")
                self.refresh_system_info()
            else:
                self.update_log(f"❌ 验证失败: {result.stderr}")
                self.install_status.value = "❌ 验证失败"
                self.install_status.color = ft.Colors.RED
                
        except Exception as e:
            self.update_log(f"❌ 验证失败: {e}")
            self.install_status.value = "❌ 验证失败"
            self.install_status.color = ft.Colors.RED
    
    def update_log(self, message):
        """更新日志"""
        def update():
            current_log = self.install_log.value
            if current_log:
                self.install_log.value = current_log + "\n" + message
            else:
                self.install_log.value = message
            self.page.update()
        
        self.page.run_thread(update)
    
    def update_status(self, message, color=ft.Colors.BLACK):
        """更新状态"""
        def update():
            self.install_status.value = message
            self.install_status.color = color
            self.page.update()
        
        self.page.run_thread(update)
    
    def refresh_system_info(self):
        """刷新系统信息"""
        def update():
            try:
                # 重新获取系统信息
                self.system_info = self.get_system_info()
                
                # 重新生成版本信息
                self.torch_versions = self.generate_torch_versions()
                
                # 重新构建UI
                self.page.controls.clear()
                self.build_ui()
                self.page.update()
                
                self.update_log("🔄 系统信息已刷新")
            except Exception as e:
                self.update_log(f"❌ 刷新系统信息失败: {e}")
        
        self.page.run_thread(update)

def main(page: ft.Page):
    """主函数"""
    TorchDragInstaller(page)

if __name__ == "__main__":
    ft.app(target=main)
