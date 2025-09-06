#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyTorch版本选择器 - 智能推荐版
根据显卡和驱动信息，智能推荐最适合的CUDA torch版本
"""

import flet as ft
import subprocess
import sys
import os
import threading
from pathlib import Path
import json
import re

class TorchVersionSelector:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PyTorch版本选择器 - 系统建议"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1000
        self.page.window_height = 900
        self.page.window_resizable = True
        
        # 获取系统信息
        self.system_info = self.get_system_info()
        
        # 可用的PyTorch版本配置
        self.torch_versions = {
            "CUDA 11.8 (RTX 30系)": {
                "torch": "torch==2.5.1+cu118",
                "torchvision": "torchvision==0.20.1+cu118", 
                "torchaudio": "torchaudio==2.5.1+cu118",
                "index_url": "https://download.pytorch.org/whl/cu118",
                "description": "兼容RTX 30系列显卡",
                "recommended": False,
                "compatible_gpus": ["RTX 30", "GTX 16", "GTX 10"],
                "min_driver": "470.0"
            },
            "CUDA 12.1 (通用)": {
                "torch": "torch==2.5.1+cu121",
                "torchvision": "torchvision==0.20.1+cu121",
                "torchaudio": "torchaudio==2.5.1+cu121", 
                "index_url": "https://download.pytorch.org/whl/cu121",
                "description": "兼容大部分RTX 40系列显卡",
                "recommended": False,
                "compatible_gpus": ["RTX 40", "RTX 30", "GTX 16"],
                "min_driver": "525.0"
            },
            "CUDA 12.4 (通用)": {
                "torch": "torch==2.5.1+cu124",
                "torchvision": "torchvision==0.20.1+cu124",
                "torchaudio": "torchaudio==2.5.1+cu124",
                "index_url": "https://download.pytorch.org/whl/cu124", 
                "description": "兼容RTX 50系和40系显卡，通用版本",
                "recommended": True,
                "compatible_gpus": ["RTX 50", "RTX 40", "RTX 30"],
                "min_driver": "550.0"
            },
            "CUDA 12.6 (稳定)": {
                "torch": "torch==2.5.1+cu126",
                "torchvision": "torchvision==0.20.1+cu126",
                "torchaudio": "torchaudio==2.5.1+cu126",
                "index_url": "https://download.pytorch.org/whl/cu126",
                "description": "稳定版本，兼容RTX 50系和40系显卡",
                "recommended": False,
                "compatible_gpus": ["RTX 50", "RTX 40", "RTX 30"],
                "min_driver": "555.0"
            },
            "CUDA 12.8 (最新)": {
                "torch": "torch==2.8.0+cu128",
                "torchvision": "torchvision==0.23.0+cu128",
                "torchaudio": "torchaudio==2.8.0+cu128",
                "index_url": "https://download.pytorch.org/whl/cu128",
                "description": "支持RTX 50系列显卡的最新版本",
                "recommended": False,
                "compatible_gpus": ["RTX 50", "RTX 40"],
                "min_driver": "560.0"
            },
            "CPU版本": {
                "torch": "torch",
                "torchvision": "torchvision", 
                "torchaudio": "torchaudio",
                "index_url": "https://pypi.tuna.tsinghua.edu.cn/simple",
                "description": "纯CPU版本，无需GPU",
                "recommended": False,
                "compatible_gpus": ["所有"],
                "min_driver": "无要求"
            }
        }
        
        # 智能推荐
        self.recommended_version = self.get_recommended_version()
        
        self.selected_version = None
        self.install_progress = None
        self.install_status = None
        self.install_log = None
        
        self.build_ui()
    
    def get_system_info(self):
        """获取系统信息"""
        info = {
            "gpu_name": "未检测到",
            "gpu_memory": "未知",
            "cuda_version": "未检测到",
            "driver_version": "未知",
            "gpu_series": "未知"
        }
        
        try:
            # 获取GPU信息
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split(', ')
                    if len(parts) >= 3:
                        info["gpu_name"] = parts[0].strip()
                        info["gpu_memory"] = f"{parts[1].strip()} MB"
                        info["driver_version"] = parts[2].strip()
                        
                        # 检测GPU系列
                        gpu_name = info["gpu_name"].upper()
                        if "RTX 50" in gpu_name:
                            info["gpu_series"] = "RTX 50"
                        elif "RTX 40" in gpu_name:
                            info["gpu_series"] = "RTX 40"
                        elif "RTX 30" in gpu_name:
                            info["gpu_series"] = "RTX 30"
                        elif "GTX 16" in gpu_name:
                            info["gpu_series"] = "GTX 16"
                        elif "GTX 10" in gpu_name:
                            info["gpu_series"] = "GTX 10"
            
            # 获取CUDA版本
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0 and result.stdout.strip():
                driver_version = result.stdout.strip()
                # 根据驱动版本估算CUDA版本
                try:
                    driver_major = int(driver_version.split('.')[0])
                    if driver_major >= 560:
                        info["cuda_version"] = "12.8+"
                    elif driver_major >= 550:
                        info["cuda_version"] = "12.4+"
                    elif driver_major >= 525:
                        info["cuda_version"] = "12.1+"
                    elif driver_major >= 470:
                        info["cuda_version"] = "11.8+"
                    else:
                        info["cuda_version"] = "11.8以下"
                except:
                    pass
                    
        except Exception as e:
            print(f"获取系统信息失败: {e}")
        
        return info
    
    def get_recommended_version(self):
        """根据系统信息推荐最适合的版本"""
        gpu_series = self.system_info["gpu_series"]
        driver_version = self.system_info["driver_version"]
        cuda_version = self.system_info["cuda_version"]
        
        # 根据驱动版本和CUDA版本智能推荐
        try:
            driver_major = int(driver_version.split('.')[0])
            
            # 优先根据检测到的CUDA版本推荐
            if "12.8+" in cuda_version and driver_major >= 560:
                if gpu_series in ["RTX 50", "RTX 40"]:
                    return "CUDA 12.8 (最新)"  # 支持最新CUDA的显卡
                else:
                    return "CUDA 12.6 (稳定)"  # 其他显卡使用12.6
            elif "12.6+" in cuda_version and driver_major >= 555:
                return "CUDA 12.6 (稳定)"  # 稳定版本，兼容性好
            elif "12.4+" in cuda_version and driver_major >= 550:
                return "CUDA 12.4 (通用)"  # 通用版本，兼容性好
            elif "12.1+" in cuda_version and driver_major >= 525:
                return "CUDA 12.1 (通用)"  # 通用版本
            elif "11.8+" in cuda_version and driver_major >= 470:
                return "CUDA 11.8 (RTX 30系)"  # 稳定版本
            else:
                # 根据GPU系列回退推荐
                if gpu_series == "RTX 50":
                    return "CUDA 12.6 (稳定)"  # RTX 50系列推荐12.6
                elif gpu_series == "RTX 40":
                    return "CUDA 12.6 (稳定)"  # RTX 40系列推荐12.6
                elif gpu_series == "RTX 30":
                    return "CUDA 12.1 (通用)"  # RTX 30系列推荐12.1
                elif gpu_series in ["GTX 16", "GTX 10"]:
                    return "CUDA 11.8 (RTX 30系)"  # GTX系列推荐11.8
                else:
                    return "CPU版本"  # 未检测到GPU时推荐CPU版本
                    
        except:
            # 解析失败时的回退逻辑
            if gpu_series == "RTX 50":
                return "CUDA 12.6 (稳定)"
            elif gpu_series == "RTX 40":
                return "CUDA 12.6 (稳定)"
            elif gpu_series == "RTX 30":
                return "CUDA 12.1 (通用)"
            elif gpu_series in ["GTX 16", "GTX 10"]:
                return "CUDA 11.8 (RTX 30系)"
            else:
                return "CPU版本"
    
    def build_ui(self):
        """构建用户界面"""
        # 标题
        title = ft.Text(
            "PyTorch版本选择器 - 系统建议",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        # 系统信息显示
        system_info_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("系统信息", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"GPU: {self.system_info['gpu_name']}", size=14),
                    ft.Text(f"GPU系列: {self.system_info['gpu_series']}", size=14),
                    ft.Text(f"显存: {self.system_info['gpu_memory']}", size=14),
                    ft.Text(f"驱动版本: {self.system_info['driver_version']}", size=14),
                    ft.Text(f"CUDA版本: {self.system_info['cuda_version']}", size=14),
                ], tight=True),
                padding=15
            )
        )
        
        # 建议信息
        recommended_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE),
                        ft.Text("系统建议", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
                    ]),
                    ft.Text(f"根据您的硬件配置，建议使用: {self.recommended_version}", size=14),
                    ft.Text("此版本与您的显卡和驱动兼容性较好", size=12, color=ft.Colors.GREY_600),
                ], tight=True),
                padding=15
            ),
            color=ft.Colors.BLUE_100
        )
        
        # 创建Radio选项列表
        radio_options = []
        for version_name, config in self.torch_versions.items():
            # 检查兼容性
            is_compatible = self.check_compatibility(version_name, config)
            is_recommended = version_name == self.recommended_version
            
            # 创建Radio选项
            radio_option = ft.Radio(
                value=version_name,
                label=version_name
            )
            radio_options.append(radio_option)
        
        # 创建Radio组
        self.radio_group = ft.RadioGroup(
            content=ft.Column(radio_options, spacing=10),
            on_change=self.on_radio_change
        )
        
        
        # 安装按钮
        self.install_btn = ft.ElevatedButton(
            "安装选中的版本",
            on_click=self.start_install,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE
            )
        )
        
        # 进度条
        self.install_progress = ft.ProgressBar(
            width=400,
            visible=False
        )
        
        # 状态文本
        self.install_status = ft.Text(
            "请选择一个PyTorch版本",
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
            width=700,
            padding=10,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
            visible=False
        )
        
        # 主布局
        main_column = ft.Column([
            title,
            system_info_card,
            recommended_card,
            ft.Divider(),
            ft.Text("选择PyTorch版本:", size=16, weight=ft.FontWeight.BOLD),
            self.radio_group,
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
    
    def check_compatibility(self, version_name, config):
        """检查版本兼容性"""
        if version_name == "CPU版本":
            return True
        
        gpu_series = self.system_info["gpu_series"]
        driver_version = self.system_info["driver_version"]
        
        # 检查GPU兼容性
        gpu_compatible = any(series in gpu_series for series in config["compatible_gpus"])
        
        # 检查驱动版本
        try:
            min_driver = config["min_driver"]
            if min_driver == "无要求":
                return gpu_compatible
            
            # 简单的驱动版本比较
            current_driver = float(driver_version.split('.')[0] + '.' + driver_version.split('.')[1])
            min_driver_float = float(min_driver)
            
            return gpu_compatible and current_driver >= min_driver_float
        except:
            return gpu_compatible
    
    def on_radio_change(self, e):
        """Radio组变化时的回调"""
        self.selected_version = e.control.value
        self.install_btn.disabled = False
        self.install_status.value = f"已选择: {self.selected_version}"
        self.install_status.color = ft.Colors.BLUE
        self.page.update()
    
    def select_version(self, version_name):
        """选择版本"""
        self.selected_version = version_name
        self.install_btn.disabled = False
        self.install_status.value = f"已选择: {version_name}"
        self.install_status.color = ft.Colors.BLUE
        self.page.update()
    
    def start_install(self, e):
        """开始安装"""
        if not self.selected_version:
            return
        
        # 更新UI状态
        self.install_btn.disabled = True
        self.install_btn.text = "安装中..."
        self.install_progress.visible = True
        self.install_status.value = f"正在安装 {self.selected_version}..."
        self.install_status.color = ft.Colors.ORANGE
        
        # 显示日志容器
        self.log_container.visible = True
        
        self.page.update()
        
        # 在后台线程中执行安装
        threading.Thread(target=self.install_torch, daemon=True).start()
    
    def install_torch(self):
        """安装PyTorch"""
        try:
            config = self.torch_versions[self.selected_version]
            python_exe = Path("python_env/python.exe")
            
            if not python_exe.exists():
                self.update_log("❌ Python可执行文件不存在")
                return
            
            self.update_log(f"开始安装 {self.selected_version}...")
            self.update_log(f"使用Python: {python_exe}")
            self.update_log(f"下载地址: {config['index_url']}")
            
            # 卸载现有版本
            self.update_log("卸载现有PyTorch...")
            subprocess.run([
                str(python_exe), "-m", "pip", "uninstall", 
                "torch", "torchvision", "torchaudio", "-y"
            ], check=False)
            
            # 安装新版本
            self.update_log("安装新版本...")
            cmd = [
                str(python_exe), "-m", "pip", "install",
                config["torch"], config["torchvision"], config["torchaudio"],
                "--index-url", config["index_url"]
            ]
            
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
                self.update_log("✅ 安装成功！")
                self.install_status.value = f"✅ {self.selected_version} 安装成功！"
                self.install_status.color = ft.Colors.GREEN
                
                # 验证安装
                self.verify_installation()
            else:
                self.update_log("❌ 安装失败")
                self.install_status.value = f"❌ {self.selected_version} 安装失败"
                self.install_status.color = ft.Colors.RED
                
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
                self.update_log("验证结果:")
                self.update_log(result.stdout)
            else:
                self.update_log(f"验证失败: {result.stderr}")
                
        except Exception as e:
            self.update_log(f"验证失败: {e}")
    
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

def main(page: ft.Page):
    """主函数"""
    TorchVersionSelector(page)

if __name__ == "__main__":
    ft.app(target=main)