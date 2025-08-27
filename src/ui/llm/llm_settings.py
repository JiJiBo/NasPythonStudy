import flet as ft
from src.db.llm_config_db import LLMConfigDB
from src.utils.ChatUtils import AIRequestHandler, ai_handler


def llm_setting_page(page: ft.Page, on_back=None):
    db = LLMConfigDB()
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
        if on_back:
            on_back(page)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("返回主页"))
            page.snack_bar.open = True
            page.update()

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=back_click),
        title=ft.Text("LLM 模型设置", size=20, weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.GREEN_50,
    )

    # 先获取最新配置
    latest_config = db.get_current_config() or db.get_latest_config_by_model("deepseek")

    # 设置模型下拉框的默认值
    model_dropdown = ft.Dropdown(
        label="选择模型类型",
        options=[
            ft.dropdown.Option("deepseek"),
            ft.dropdown.Option("OpenAI"),
            ft.dropdown.Option("ollama"),
        ],
        value=latest_config.get("provider") if latest_config else "deepseek",
        width=380,
    )

    # 输入框
    api_key_field = ft.TextField(label="API Key", width=380, password=True, can_reveal_password=True)
    base_url_field = ft.TextField(label="Base URL", width=380, value="https://api.openai.com/v1")
    addr_field = ft.TextField(label="服务地址", width=380, value="http://localhost:11434")
    ollama_model_field = ft.TextField(label="模型名", width=380, value="")
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
                "deepseek-chat" if selected == "deepseek" else None),
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

    model_dropdown.on_change = on_model_change

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
                        ft.ElevatedButton("保存为新配置", on_click=save_new_config),
                        ft.ElevatedButton("清空输入", on_click=lambda e: clear_fields()),
                    ], spacing=10),
                ])
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
