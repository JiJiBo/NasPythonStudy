import flet as ft
from src.db.llm_config_db import LLMConfigDB
from src.str.APP_CONFIG import ai_handler
from src.utils.LocalModelManager import local_model_manager


def llm_setting_page(page: ft.Page, on_back=None):
    db = LLMConfigDB()
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
            else:
                brief = current.get("base_url") or ""
            current_config_text.value = f"当前使用：{provider} | {brief}"
        else:
            current_config_text.value = "当前使用：无"
        page.update()

    refresh_current_config_display()

    # 返回按钮
    def back_click(e):
        # 返回时恢复底部导航栏
        if previous_navigation_bar is not None:
            page.navigation_bar = previous_navigation_bar
        # 恢复进入前的 AppBar（可能为 None）
        page.appbar = previous_appbar
        if on_back:
            # 假定 on_back 支持可选参数 selected_index，用于回到主页并选中“设置”标签
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
            ft.dropdown.Option("deepseek"),
            ft.dropdown.Option("OpenAI"),
            ft.dropdown.Option("ollama"),
            ft.dropdown.Option("local"),
        ],
        value=latest_config.get("provider") if latest_config else "deepseek",
        width=380,
    )

    # 输入框
    api_key_field = ft.TextField(label="API Key", width=380, password=True, can_reveal_password=True)
    base_url_field = ft.TextField(label="Base URL", width=380, value="https://api.openai.com/v1")
    addr_field = ft.TextField(label="服务地址", width=380, value="http://localhost:11434")
    ollama_model_field = ft.TextField(label="模型名", width=380, value="")
    
    # 本地模型相关控件
    local_model_dropdown = ft.Dropdown(
        label="选择本地模型",
        width=400,
        options=[],
        expand=True
    )
    local_model_status = ft.Text("", size=12, color=ft.Colors.GREY, width=400)
    local_model_progress = ft.ProgressBar(width=400, visible=False)
    local_model_progress_text = ft.Text("", size=12, width=400)
    
    # 本地模型管理按钮 - 先创建按钮，稍后绑定事件
    download_btn = ft.ElevatedButton("下载模型")
    load_btn = ft.ElevatedButton("加载模型")
    delete_btn = ft.ElevatedButton("删除模型")
    
    local_model_buttons = ft.Column([
        ft.Row([download_btn, load_btn], spacing=10),
        ft.Row([delete_btn], spacing=10)
    ], spacing=5)
    
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
        elif model_dropdown.value == "local":
            config_container.controls.extend([
                local_model_dropdown,
                local_model_status,
                local_model_progress,
                local_model_progress_text,
                local_model_buttons
            ])
            refresh_local_model_list()

    # 刷新本地模型列表
    def refresh_local_model_list():
        available_models = local_model_manager.get_available_models()
        installed_models = local_model_manager.get_installed_models()
        
        local_model_dropdown.options.clear()
        
        for model_name, model_info in available_models.items():
            is_installed = any(m.name == model_name for m in installed_models)
            status = "✓" if is_installed else "✗"
            size_mb = model_info.size // (1024 * 1024)
            
            # 简化显示文本，避免过长
            display_name = model_name.replace("qwen2.5-coder-1.5b-", "Qwen-")
            text = f"{display_name} ({size_mb}MB) {status}"
            
            local_model_dropdown.options.append(
                ft.dropdown.Option(
                    key=model_name,
                    text=text,
                    disabled=not is_installed
                )
            )
        
        # 设置当前选中的模型
        current_status = local_model_manager.get_model_status()
        if current_status["current_model"]:
            local_model_dropdown.value = current_status["current_model"]
        
        update_local_model_status()
        page.update()
    
    # 更新本地模型状态显示
    def update_local_model_status():
        current_status = local_model_manager.get_model_status()
        if current_status["current_model"]:
            local_model_status.value = f"当前使用: {current_status['current_model']}"
            local_model_status.color = ft.Colors.GREEN
        else:
            local_model_status.value = "未选择模型"
            local_model_status.color = ft.Colors.ORANGE
    
    # 下载模型
    def download_model(model_name):
        print(f"开始下载模型: {model_name}")  # 调试信息
        
        def progress_callback(name, progress, downloaded, total):
            local_model_progress.visible = True
            local_model_progress.value = progress / 100
            local_model_progress_text.value = f"下载中: {progress:.1f}% ({downloaded//1024//1024}MB/{total//1024//1024}MB)"
            print(f"下载进度: {progress:.1f}%")  # 调试信息
            page.update()
        
        def error_callback(error):
            local_model_progress.visible = False
            local_model_progress_text.value = f"下载失败: {error}"
            print(f"下载错误: {error}")  # 调试信息
            page.snack_bar = ft.SnackBar(ft.Text(f"下载失败: {error}"))
            page.snack_bar.open = True
            page.update()
        
        def success_callback():
            local_model_progress.visible = False
            local_model_progress_text.value = "下载完成"
            print(f"模型下载完成: {model_name}")  # 调试信息
            page.snack_bar = ft.SnackBar(ft.Text(f"模型 {model_name} 下载完成"))
            page.snack_bar.open = True
            # 刷新模型列表
            refresh_local_model_list()
            page.update()
        
        try:
            # 显示下载开始状态
            local_model_progress.visible = True
            local_model_progress.value = 0
            local_model_progress_text.value = "准备下载..."
            page.update()
            
            # 开始下载
            success = local_model_manager.download_model(model_name, progress_callback, error_callback)
            if success:
                # 下载完成后调用成功回调
                success_callback()
            else:
                error_callback("下载启动失败")
                
        except Exception as e:
            error_callback(f"下载异常: {str(e)}")
    
    # 加载模型
    def load_model(model_name):
        if local_model_manager.load_model(model_name):
            update_local_model_status()
            page.snack_bar = ft.SnackBar(ft.Text(f"已加载模型: {model_name}"))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"加载模型失败: {model_name}"))
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
            if model_dropdown.value == "local":
                local_model_dropdown.value = latest.get("model") or ""
            selected_config_id["id"] = latest.get("id")
        else:
            clear_fields()
        page.update()

    # 清空输入框
    def clear_fields():
        api_key_field.value = ""
        base_url_field.value = "https://api.openai.com/v1"
        addr_field.value = "http://localhost:11434"
        ollama_model_field.value = ""
        # 不清空本地模型相关控件，保持状态
        page.update()

    # 保存新配置
    def save_new_config(e):
        selected = model_dropdown.value
        model_name = None
        
        if selected == "ollama":
            model_name = ollama_model_field.value
        elif selected == "deepseek":
            model_name = "deepseek-chat"
        elif selected == "local":
            model_name = local_model_dropdown.value
            if model_name:
                # 加载选中的本地模型
                load_model(model_name)
        
        new_id = db.save_config(
            provider=selected,
            api_key=api_key_field.value if selected in ["OpenAI", "deepseek"] else None,
            base_url=base_url_field.value if selected == "OpenAI" else None,
            addr=addr_field.value if selected == "ollama" else None,
            model=model_name,
        )
        db.set_current_config(new_id)
        selected_config_id["id"] = new_id
        refresh_current_config_display()
        page.snack_bar = ft.SnackBar(ft.Text(f"保存为新配置（id={new_id}）"))
        page.snack_bar.open = True
        page.update()
        ai_handler.refresh_config()

    # 模型切换
    def on_model_change(e):
        selected_config_id["id"] = None
        render_config_fields()
        load_latest_config()

    # 显示下载对话框
    def show_download_dialog():
        available_models = local_model_manager.get_available_models()
        installed_models = local_model_manager.get_installed_models()
        installed_names = [m.name for m in installed_models]
        
        # 创建可下载的模型列表
        download_options = []
        for model_name, model_info in available_models.items():
            if model_name not in installed_names:
                size_mb = model_info.size // (1024 * 1024)
                # 简化显示文本
                display_name = model_name.replace("qwen2.5-coder-1.5b-", "Qwen-")
                short_desc = model_info.description[:20] + "..." if len(model_info.description) > 20 else model_info.description
                text = f"{display_name} ({size_mb}MB) - {short_desc}"
                
                download_options.append(
                    ft.dropdown.Option(
                        key=model_name,
                        text=text
                    )
                )
        
        if not download_options:
            page.snack_bar = ft.SnackBar(ft.Text("所有模型都已安装"))
            page.snack_bar.open = True
            page.update()
            return
        
        download_dropdown = ft.Dropdown(
            options=download_options,
            width=400
        )
        
        def confirm_download(e):
            if download_dropdown.value:
                print(f"开始下载模型: {download_dropdown.value}")  # 调试信息
                download_model(download_dropdown.value)
                page.close(dlg)
        
        def cancel_download(e):
            page.close(dlg)
        
        dlg = ft.AlertDialog(
            title=ft.Text("下载模型"),
            content=ft.Column([
                ft.Text("选择要下载的模型:", size=14),
                download_dropdown
            ], spacing=10),
            actions=[
                ft.ElevatedButton("下载", on_click=confirm_download),
                ft.TextButton("取消", on_click=cancel_download)
            ]
        )
        
        print("打开下载对话框")  # 调试信息
        page.dialog = dlg
        page.open(dlg)
        page.update()
    
    # 显示删除对话框
    def show_delete_dialog():
        installed_models = local_model_manager.get_installed_models()
        
        if not installed_models:
            page.snack_bar = ft.SnackBar(ft.Text("没有已安装的模型"))
            page.snack_bar.open = True
            page.update()
            return
        
        delete_options = []
        for model_info in installed_models:
            size_mb = model_info.size // (1024 * 1024)
            delete_options.append(
                ft.dropdown.Option(
                    key=model_info.name,
                    text=f"{model_info.name} ({size_mb}MB)"
                )
            )
        
        delete_dropdown = ft.Dropdown(
            label="选择要删除的模型",
            options=delete_options,
            width=400
        )
        
        def confirm_delete(e):
            if delete_dropdown.value:
                if local_model_manager.delete_model(delete_dropdown.value):
                    page.snack_bar = ft.SnackBar(ft.Text(f"已删除模型: {delete_dropdown.value}"))
                    refresh_local_model_list()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("删除失败"))
                page.snack_bar.open = True
                page.close(dlg)
                page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("删除模型"),
            content=delete_dropdown,
            actions=[
                ft.TextButton("删除", on_click=confirm_delete),
                ft.TextButton("取消", on_click=lambda e: page.close(dlg))
            ]
        )
        page.dialog = dlg
        page.open(dlg)
        page.update()

    # 模型切换事件
    def on_model_change(e):
        selected_config_id["id"] = None
        render_config_fields()
        load_latest_config()
    
    model_dropdown.on_change = on_model_change
    
    # 绑定按钮事件
    def on_download_click(e):
        print("下载按钮被点击!")
        page.snack_bar = ft.SnackBar(ft.Text("下载按钮被点击!"))
        page.snack_bar.open = True
        page.update()
        show_download_dialog()
    
    def on_load_click(e):
        print("加载按钮被点击!")
        if local_model_dropdown.value:
            load_model(local_model_dropdown.value)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("请先选择模型"))
            page.snack_bar.open = True
            page.update()
    
    def on_delete_click(e):
        print("删除按钮被点击!")
        show_delete_dialog()
    
    download_btn.on_click = on_download_click
    load_btn.on_click = on_load_click
    delete_btn.on_click = on_delete_click
    
    render_config_fields()
    load_latest_config()
    
    # 构建主界面
    page.add(
        ft.Container(
            content=ft.Column([
                current_config_text,
                ft.Container(
                    content=ft.Column([
                        model_dropdown,
                        config_container,
                        ft.Row([
                            ft.ElevatedButton("保存为新配置", on_click=save_new_config),
                            ft.ElevatedButton("清空输入", on_click=lambda e: clear_fields()),
                        ], spacing=10),
                    ], spacing=8),
                    width=450,  # 固定宽度确保有足够空间
                    padding=ft.Padding(10, 10, 10, 10)
                ),
                ft.Divider(),
            ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(20, 20, 20, 20)
        )
    )
