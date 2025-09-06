import flet as ft
from src.db.llm_config_db import LLMConfigDB
from src.str.APP_CONFIG import ai_handler
from src.utils.ModelManager import model_manager

# 全局状态管理
class DownloadState:
    IDLE = "idle"           # 空闲状态
    DOWNLOADING = "downloading"  # 正在下载
    PAUSED = "paused"       # 暂停/中断
    COMPLETED = "completed"  # 下载完成
    FAILED = "failed"       # 下载失败

# 全局变量管理下载状态
_download_states = {}  # {model_name: DownloadState}
_timer_running = False  # 定时器是否正在运行


def llm_setting_page(page: ft.Page, on_back=None):
    db = LLMConfigDB()
    
    # 状态管理函数
    def get_download_state(model_name):
        """获取模型下载状态"""
        return _download_states.get(model_name, DownloadState.IDLE)
    
    def set_download_state(model_name, state):
        """设置模型下载状态"""
        _download_states[model_name] = state
    
    def is_downloading(model_name):
        """检查模型是否正在下载"""
        return get_download_state(model_name) == DownloadState.DOWNLOADING
    
    def can_resume_download(model_name):
        """检查是否可以恢复下载"""
        state = get_download_state(model_name)
        return state in [DownloadState.PAUSED, DownloadState.FAILED]
    
    def clear_download_state(model_name):
        """清除模型下载状态"""
        if model_name in _download_states:
            del _download_states[model_name]
    
    # 线程安全的UI更新函数
    def safe_update_ui():
        """线程安全的UI更新函数"""
        try:
            page.update()
            return True
        except Exception as e:
            print(f"UI更新失败: {e}")
            return False
    
    # UI更新节流机制
    _last_ui_update = 0
    _ui_update_interval = 0.5  # 最多每0.5秒更新一次UI
    
    def throttled_update_ui():
        """节流的UI更新函数"""
        import time
        global _last_ui_update
        
        current_time = time.time()
        if current_time - _last_ui_update >= _ui_update_interval:
            _last_ui_update = current_time
            return safe_update_ui()
        return True
    
    def force_refresh_ui():
        """强制刷新UI"""
        try:
            # 强制更新所有控件
            model_status_text.update()
            mirror_status_text.update()
            download_button.update()
            delete_button.update()
            page.update()
            return True
        except Exception as e:
            print(f"强制刷新UI失败: {e}")
            return False
    
    # 进入页面时检查并同步下载状态
    def sync_download_states():
        """同步所有模型的下载状态"""
        from src.utils.DownloadStateManager import download_state_manager
        
        for model_name in ["qwen2.5-0.5b", "tinyllama-1.1b"]:
            # 首先检查模型是否已下载
            if model_manager.is_model_downloaded(model_name):
                set_download_state(model_name, DownloadState.COMPLETED)
                continue
            
            # 检查 download_state_manager 中的状态
            download_state = download_state_manager.get_download_state(model_name)
            
            if download_state:
                # 有下载状态记录
                if download_state["status"] == "downloading":
                    set_download_state(model_name, DownloadState.DOWNLOADING)
                elif download_state["status"] == "paused":
                    set_download_state(model_name, DownloadState.PAUSED)
                elif download_state["status"] == "failed":
                    set_download_state(model_name, DownloadState.FAILED)
                elif download_state["status"] == "completed":
                    set_download_state(model_name, DownloadState.COMPLETED)
            elif model_manager.is_downloading(model_name):
                # 检查 model_manager 中的状态
                progress_info = model_manager.get_download_progress(model_name)
                if progress_info["status"] == "downloading":
                    set_download_state(model_name, DownloadState.DOWNLOADING)
                elif progress_info["status"] == "failed":
                    set_download_state(model_name, DownloadState.FAILED)
            else:
                set_download_state(model_name, DownloadState.IDLE)
        
        # 同步完成后，立即更新当前选中模型的状态显示
        # 注意：这里不能直接引用model_dropdown，因为还没有定义
        # 状态同步会在页面加载完成后通过其他机制触发UI更新
        
        # 注意：这里不能直接引用progress_listener_callback，因为还没有定义
        # 监听器订阅会在页面加载完成后通过其他机制处理
    
    # 立即同步状态
    sync_download_states()
    
    # 进度监听器回调函数
    def progress_listener_callback(filename, downloaded, total):
        """进度监听器回调"""
        if total > 0:
            progress = (downloaded / total) * 100
            current_mirror = model_manager.get_current_mirror()
            model_status_text.value = f"正在下载 {filename}: {progress:.1f}%"
            mirror_status_text.value = f"当前镜像: {current_mirror}"
            
            # 使用强制刷新UI
            force_refresh_ui()
    
    # 状态监听器回调函数
    def status_listener_callback(model_name_param, status):
        """状态监听器回调"""
        if model_dropdown.value == "local_model" and local_model_dropdown.value:
            current_model = local_model_dropdown.value
            if current_model == model_name_param:
                # 更新状态
                if status == "completed":
                    set_download_state(model_name_param, DownloadState.COMPLETED)
                    model_status_text.value = "✓ 模型下载完成！"
                    model_status_text.color = ft.Colors.GREEN
                    download_button.text = "重新下载"
                    download_button.disabled = False
                    delete_button.disabled = False
                    page.snack_bar = ft.SnackBar(ft.Text("模型下载成功！"))
                    page.snack_bar.open = True
                elif status == "failed":
                    set_download_state(model_name_param, DownloadState.FAILED)
                    model_status_text.value = "✗ 模型下载失败"
                    model_status_text.color = ft.Colors.RED
                    download_button.text = "重新下载"
                    download_button.disabled = False
                    page.snack_bar = ft.SnackBar(ft.Text("模型下载失败，请检查网络连接"))
                    page.snack_bar.open = True
                
                # 强制刷新UI
                force_refresh_ui()
    
    # 订阅正在下载和暂停的模型的监听器
    def subscribe_downloading_models():
        """订阅正在下载和暂停的模型的监听器"""
        # 订阅状态监听器
        model_manager.subscribe_status(status_listener_callback)
        
        for model_name in ["qwen2.5-0.5b", "tinyllama-1.1b"]:
            current_state = get_download_state(model_name)
            if current_state in [DownloadState.DOWNLOADING, DownloadState.PAUSED]:
                model_manager.subscribe_progress(model_name, progress_listener_callback)
    
    # 进入本页面时，暂存并移除底部导航栏
    previous_navigation_bar = getattr(page, "navigation_bar", None)
    if previous_navigation_bar is not None:
        page.navigation_bar = None
        page.update()

    # 暂存进入前的 AppBar，并在本页设置 AppBar
    previous_appbar = getattr(page, "appbar", None)
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: back_click(e)),
        title=ft.Text("LLM 模型设置", size=20, weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.GREEN_50,
    )

    page.clean()

    selected_config_id = {"id": None}  # 当前载入的配置id

    # 显示当前配置
    current_config_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)

    def refresh_current_config_display():
        current = db.get_current_config()
        if current:
            provider = current.get("provider")
            if provider in ["OpenAI", "deepseek"]:
                api_key = current.get("api_key") or ""
                brief = f"{api_key[:4]}{'*' * (len(api_key) - 4)}" if api_key else ""
            elif provider == "ollama":
                addr = current.get("addr") or ""
                model_name = current.get("model") or ""
                brief = f"{addr} | 模型: {model_name}"
            elif provider == "local_model":
                model_name = current.get("model") or ""
                if model_manager.is_model_downloaded(model_name):
                    size = model_manager.format_size(model_manager.get_model_size(model_name))
                    brief = f"本地模型: {model_name} ({size})"
                else:
                    brief = f"本地模型: {model_name} (未下载)"
            else:
                brief = current.get("base_url") or ""
            current_config_text.value = f"当前使用：{provider} | {brief}"
        else:
            current_config_text.value = "当前使用：无"
        page.update()

    refresh_current_config_display()

    # 返回按钮
    def back_click(e):
        # 停止定时器
        stop_timer()
        
        # 取消所有进度监听器订阅
        for model_name in ["qwen2.5-0.5b", "tinyllama-1.1b"]:
            model_manager.unsubscribe_progress(model_name, progress_listener_callback)
        
        # 取消状态监听器订阅
        model_manager.unsubscribe_status(status_listener_callback)
        
        # 返回时恢复底部导航栏
        if previous_navigation_bar is not None:
            page.navigation_bar = previous_navigation_bar
        # 恢复进入前的 AppBar（可能为 None）
        page.appbar = previous_appbar
        if on_back:
            # 假定 on_back 支持可选参数 selected_index，用于回到主页并选中"设置"标签
            try:
                on_back(page, selected_index=2)
            except TypeError:
                on_back(page)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("返回主页"))
            page.snack_bar.open = True
            page.update()

    # 使用 AppBar，不在内容区域放返回按钮

    # 先获取最新配置
    latest_config = db.get_current_config() or db.get_latest_config_by_model("deepseek")

    # 设置模型下拉框的默认值
    model_dropdown = ft.Dropdown(
        label="选择模型类型",
        options=[
            ft.dropdown.Option("deepseek", "DeepSeek"),
            ft.dropdown.Option("OpenAI", "OpenAI"),
            ft.dropdown.Option("ollama", "Ollama"),
            ft.dropdown.Option("local_model", "本地模型"),
        ],
        value=latest_config.get("provider") if latest_config else "deepseek",
        width=380,
    )

    # 输入框
    api_key_field = ft.TextField(label="API密钥", width=380, password=True, can_reveal_password=True)
    base_url_field = ft.TextField(label="基础URL", width=380, value="https://api.openai.com/v1")
    addr_field = ft.TextField(label="服务地址", width=380, value="http://localhost:11434")
    ollama_model_field = ft.TextField(label="模型名称", width=380, value="")
    
    # 本地模型选择
    local_model_dropdown = ft.Dropdown(
        label="选择本地模型",
        options=[
            ft.dropdown.Option("qwen2.5-0.5b", "Qwen2.5-0.5B (1GB) - 轻量级中文对话模型"),
            ft.dropdown.Option("qwen2.5-1.5b", "Qwen2.5-1.5B (3GB) - 中等规模中文对话模型"),
            ft.dropdown.Option("qwen2.5-3b", "Qwen2.5-3B (6GB) - 高性能中文对话模型"),
            ft.dropdown.Option("tinyllama-1.1b", "TinyLlama-1.1B (2GB) - 英文对话模型"),
        ],
        width=380,
    )
    
    # 模型管理按钮
    download_button = ft.ElevatedButton("下载模型", width=120)
    delete_button = ft.ElevatedButton("删除模型", width=120)
    model_status_text = ft.Text("", size=12, color=ft.Colors.GREEN)
    mirror_status_text = ft.Text("", size=10, color=ft.Colors.BLUE)
    
    config_container = ft.Column(spacing=8)

    # 渲染输入框
    def render_config_fields():
        config_container.controls.clear()
        if model_dropdown.value == "OpenAI":
            config_container.controls.extend([api_key_field, base_url_field])
        elif model_dropdown.value == "deepseek":
            config_container.controls.append(api_key_field)
        elif model_dropdown.value == "ollama":
            config_container.controls.extend([addr_field, ollama_model_field])
        elif model_dropdown.value == "local_model":
            config_container.controls.extend([
                local_model_dropdown,
                ft.Row([download_button, delete_button], spacing=10),
                model_status_text,
                mirror_status_text
            ])

    # 更新模型状态显示
    def update_model_status():
        if model_dropdown.value == "local_model" and local_model_dropdown.value:
            model_name = local_model_dropdown.value
            current_state = get_download_state(model_name)
            
            
            # 根据状态机更新UI
            if current_state == DownloadState.DOWNLOADING:
                # 正在下载 - 使用专门的进度显示函数
                update_download_progress_display(model_name)
                
                download_button.text = "正在下载"
                download_button.disabled = True
                delete_button.disabled = True
            elif current_state == DownloadState.FAILED:
                # 下载失败
                progress_info = model_manager.get_download_progress(model_name)
                model_status_text.value = f"下载失败: {progress_info['message']}"
                model_status_text.color = ft.Colors.RED
                download_button.text = "重新下载"
                download_button.disabled = False
                delete_button.disabled = True
            elif current_state == DownloadState.COMPLETED:
                # 下载完成
                size = model_manager.get_model_size(model_name)
                size_str = model_manager.format_size(size)
                model_status_text.value = f"✓ 模型已下载 ({size_str})"
                model_status_text.color = ft.Colors.GREEN
                download_button.text = "重新下载"
                download_button.disabled = False
                delete_button.disabled = False
            elif current_state == DownloadState.PAUSED:
                # 暂停状态
                model_status_text.value = "下载已暂停，可以恢复"
                model_status_text.color = ft.Colors.ORANGE
                download_button.text = "恢复下载"
                download_button.disabled = False
                delete_button.disabled = True
            else:  # IDLE
                # 模型未下载
                model_info = model_manager.get_model_info(model_name)
                if model_info:
                    model_status_text.value = f"模型未下载 (约{model_info['size_mb']}MB)"
                    model_status_text.color = ft.Colors.ORANGE
                    download_button.text = "下载模型"
                    delete_button.disabled = True
                else:
                    model_status_text.value = "未知模型"
                    model_status_text.color = ft.Colors.RED
            
            # 更新镜像状态
            current_mirror = model_manager.get_current_mirror()
            mirror_status_text.value = f"当前镜像: {current_mirror}"
            safe_update_ui()
    
    # 专门用于更新下载进度显示的函数
    def update_download_progress_display(model_name):
        """从状态文件更新下载进度显示"""
        if model_dropdown.value != "local_model" or local_model_dropdown.value != model_name:
            return
        
        try:
            from src.utils.DownloadStateManager import download_state_manager
            download_state = download_state_manager.get_download_state(model_name)
            
            if download_state and download_state.get("status") == "downloading":
                completed_files = download_state.get("completed_files", 0)
                total_files = download_state.get("total_files", 0)
                current_file = download_state.get("current_file")
                current_progress = download_state.get("current_file_progress", 0)
                current_total = download_state.get("current_file_total", 0)
                
                
                if current_file and current_total > 0:
                    # 显示当前文件进度
                    progress_percent = (current_progress / current_total) * 100
                    model_status_text.value = f"正在下载 {current_file}: {progress_percent:.1f}%"
                elif current_file:
                    # 显示当前文件但无进度信息
                    model_status_text.value = f"正在下载 {current_file}"
                else:
                    # 显示文件计数
                    model_status_text.value = f"已下载 {completed_files}/{total_files} 个文件"
                
                model_status_text.color = ft.Colors.BLUE
                
                # 更新镜像状态
                current_mirror = model_manager.get_current_mirror()
                mirror_status_text.value = f"当前镜像: {current_mirror}"
                
                # 强制更新UI
                safe_update_ui()
                    
        except Exception as e:
            print(f"更新下载进度显示时出错: {e}")

    # 下载模型
    def download_model(e):
        if not local_model_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("请先选择要下载的模型"))
            page.snack_bar.open = True
            page.update()
            return
        
        model_name = local_model_dropdown.value
        
        # 使用状态机检查下载状态
        current_state = get_download_state(model_name)
        if current_state == DownloadState.DOWNLOADING:
            page.snack_bar = ft.SnackBar(ft.Text("模型正在下载中，请稍候..."))
            page.snack_bar.open = True
            page.update()
            return
        
        # 检查是否是恢复下载
        is_resuming = can_resume_download(model_name)
        if is_resuming:
            # 如果是暂停状态，先恢复下载状态
            if get_download_state(model_name) == DownloadState.PAUSED:
                from src.utils.DownloadStateManager import download_state_manager
                download_state_manager.resume_download(model_name)
                set_download_state(model_name, DownloadState.DOWNLOADING)
                model_status_text.value = "恢复下载中..."
            else:
                progress_info = model_manager.get_download_progress(model_name)
                if progress_info["status"] == "downloading":
                    model_status_text.value = f"恢复下载: {progress_info['message']}"
                else:
                    model_status_text.value = "重新开始下载..."
        else:
            model_status_text.value = "正在下载模型，请稍候..."
        
        # 设置下载状态
        set_download_state(model_name, DownloadState.DOWNLOADING)
        
        # 订阅进度监听器
        model_manager.subscribe_progress(model_name, progress_listener_callback)
        
        model_status_text.color = ft.Colors.BLUE
        download_button.disabled = True
        safe_update_ui()
        
        # 调整定时器间隔为更频繁的更新
        adjust_timer_interval()
        
        
        def download_thread():
            try:
                success = model_manager.download_model(model_name)
                # 状态监听器会处理界面更新，这里不需要重复处理
                
                # 取消订阅进度监听器
                model_manager.unsubscribe_progress(model_name, progress_listener_callback)
                
                # 调整定时器间隔
                adjust_timer_interval()
            except Exception as ex:
                # 下载异常
                set_download_state(model_name, DownloadState.FAILED)
                model_status_text.value = f"✗ 下载出错: {str(ex)}"
                model_status_text.color = ft.Colors.RED
                download_button.text = "重新下载"
                download_button.disabled = False
                page.snack_bar = ft.SnackBar(ft.Text(f"下载出错: {str(ex)}"))
                page.snack_bar.open = True
                force_refresh_ui()
                
                # 取消订阅进度监听器
                model_manager.unsubscribe_progress(model_name, progress_listener_callback)
                adjust_timer_interval()
        
        import threading
        threading.Thread(target=download_thread, daemon=True).start()

    # 删除模型
    def delete_model(e):
        if not local_model_dropdown.value:
            return
        
        model_name = local_model_dropdown.value
        if model_manager.delete_model(model_name):
            model_status_text.value = "模型已删除"
            model_status_text.color = ft.Colors.ORANGE
            download_button.text = "下载模型"
            delete_button.disabled = True
            page.snack_bar = ft.SnackBar(ft.Text("模型已删除"))
            page.snack_bar.open = True
            page.update()

    # 加载最新配置
    def load_latest_config():
        latest = db.get_latest_config_by_model(model_dropdown.value)
        if latest:
            if model_dropdown.value in ["OpenAI", "deepseek"]:
                api_key_field.value = latest.get("api_key") or ""
            if model_dropdown.value == "OpenAI":
                base_url_field.value = latest.get("base_url") or "https://api.openai.com/v1"
            if model_dropdown.value == "ollama":
                addr_field.value = latest.get("addr") or "http://localhost:11434"
                ollama_model_field.value = latest.get("model") or ""
            if model_dropdown.value == "local_model":
                local_model_dropdown.value = latest.get("model") or "qwen2.5-0.5b"
                update_model_status()
            selected_config_id["id"] = latest.get("id")
        else:
            clear_fields()
        
        # 如果是本地模型，确保状态显示正确
        if model_dropdown.value == "local_model" and local_model_dropdown.value:
            update_model_status()
        
        # 订阅正在下载的模型的监听器
        subscribe_downloading_models()
        
        page.update()

    # 清空输入框
    def clear_fields():
        api_key_field.value = ""
        base_url_field.value = "https://api.openai.com/v1"
        addr_field.value = "http://localhost:11434"
        ollama_model_field.value = ""
        local_model_dropdown.value = "qwen2.5-0.5b"
        model_status_text.value = ""
        mirror_status_text.value = ""
        page.update()

    # 保存新配置
    def save_new_config(e):
        selected = model_dropdown.value
        new_id = db.save_config(
            provider=selected,
            api_key=api_key_field.value if selected in ["OpenAI", "deepseek"] else None,
            base_url=base_url_field.value if selected == "OpenAI" else None,
            addr=addr_field.value if selected == "ollama" else None,
            model=ollama_model_field.value if selected == "ollama" else (
                local_model_dropdown.value if selected == "local_model" else (
                "deepseek-chat" if selected == "deepseek" else None)),
        )
        db.set_current_config(new_id)
        selected_config_id["id"] = new_id
        refresh_current_config_display()
        page.snack_bar = ft.SnackBar(ft.Text(f"配置已保存（ID: {new_id}）"))
        page.snack_bar.open = True
        page.update()
        ai_handler.refresh_config()

    # 模型切换
    def on_model_change(e):
        selected_config_id["id"] = None
        render_config_fields()
        load_latest_config()

    # 本地模型选择变化
    def on_local_model_change(e):
        update_model_status()

    # 绑定事件
    model_dropdown.on_change = on_model_change
    local_model_dropdown.on_change = on_local_model_change
    download_button.on_click = download_model
    delete_button.on_click = delete_model

    render_config_fields()
    load_latest_config()
    page.add(
        ft.Column([
            current_config_text,
            ft.Row([
                ft.Column([
                    model_dropdown,
                    config_container,
                    ft.Row([
                        ft.ElevatedButton("保存配置", on_click=save_new_config),
                        ft.ElevatedButton("清空输入", on_click=lambda e: clear_fields()),
                    ], spacing=10),
                ])
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    # 添加定时器来更新下载状态
    def on_timer(e):
        global _timer_running
        if not _timer_running:
            return
            
        if model_dropdown.value == "local_model" and local_model_dropdown.value:
            model_name = local_model_dropdown.value
            current_state = get_download_state(model_name)
            
            # 同步状态管理器的状态
            from src.utils.DownloadStateManager import download_state_manager
            download_state = download_state_manager.get_download_state(model_name)
            
            # 检查是否有正在进行的下载（通过model_manager检查）
            is_actually_downloading = model_manager.is_downloading(model_name)
            
            # 首先检查模型是否已下载完成
            if model_manager.is_model_downloaded(model_name):
                if current_state != DownloadState.COMPLETED:
                    set_download_state(model_name, DownloadState.COMPLETED)
            elif download_state:
                # 有状态记录，同步状态
                if download_state["status"] == "downloading":
                    if current_state != DownloadState.DOWNLOADING:
                        set_download_state(model_name, DownloadState.DOWNLOADING)
                elif download_state["status"] == "failed":
                    if current_state != DownloadState.FAILED:
                        set_download_state(model_name, DownloadState.FAILED)
                elif download_state["status"] == "completed":
                    if current_state != DownloadState.COMPLETED:
                        set_download_state(model_name, DownloadState.COMPLETED)
            elif is_actually_downloading:
                # model_manager检测到正在下载，但状态管理器中没有记录
                if current_state != DownloadState.DOWNLOADING:
                    set_download_state(model_name, DownloadState.DOWNLOADING)
            elif current_state == DownloadState.DOWNLOADING:
                # 状态机显示正在下载，但实际没有下载，可能已中断
                set_download_state(model_name, DownloadState.PAUSED)
            
            # 更新UI状态
            update_model_status()
            
            # 如果正在下载，强制更新进度显示
            if current_state == DownloadState.DOWNLOADING:
                update_download_progress_display(model_name)
            
            # 动态调整定时器间隔
            adjust_timer_interval()
    
    # 启动定时器
    def start_timer():
        global _timer_running
        if not _timer_running:
            _timer_running = True
            page.on_timer = on_timer
            # 初始设置为2秒间隔
            page.timer_interval = 2
            page.update()
            print("定时器已启动")
    
    # 停止定时器
    def stop_timer():
        global _timer_running
        if _timer_running:
            _timer_running = False
            page.timer_interval = 0
            page.update()
            print("定时器已停止")
    
    # 动态调整定时器间隔
    def adjust_timer_interval():
        """根据下载状态动态调整定时器间隔"""
        global _timer_running
        if not _timer_running:
            return
        
        # 检查是否有正在下载的模型
        has_downloading = False
        for model_name in ["qwen2.5-0.5b", "tinyllama-1.1b"]:
            if get_download_state(model_name) == DownloadState.DOWNLOADING:
                has_downloading = True
                break
        
        # 如果有正在下载的模型，使用更短的间隔（1秒）
        # 否则使用较长的间隔（3秒）
        new_interval = 1 if has_downloading else 3
        
        if page.timer_interval != new_interval:
            page.timer_interval = new_interval
            print(f"定时器间隔调整为: {new_interval}秒")
    
    # 立即启动定时器
    start_timer()
