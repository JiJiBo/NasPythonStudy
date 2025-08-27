import flet as ft

from src.db.llm_config_db import LLMConfigDB


def llm_setting_page(page: ft.Page, on_back=None):
    db = LLMConfigDB()  # 初始化数据库
    page.clean()

    # 返回按钮点击
    def back_click(e):
        if on_back:
            on_back(page)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("返回主页"))
            page.snack_bar.open = True
            page.update()

    # 顶部导航栏
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=back_click),
        title=ft.Text("LLM 模型设置", size=20, weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.GREEN_50,
    )

    # 下拉框 - 选择模型
    model_dropdown = ft.Dropdown(
        label="选择模型类型",
        options=[
            ft.dropdown.Option("deepseek"),
            ft.dropdown.Option("OpenAI"),
            ft.dropdown.Option("ollama"),
        ],
        value="deepseek",
        width=300,
    )

    # 输入框（不同模型显示不同内容）
    api_key_field = ft.TextField(label="API Key", width=300, password=True, can_reveal_password=True)
    base_url_field = ft.TextField(label="Base URL", width=300, value="https://api.openai.com/v1")
    addr_field = ft.TextField(label="服务地址", width=300, value="http://localhost:11434")

    # 容器，用来切换不同的配置项
    config_container = ft.Column(spacing=10)

    # 根据选择的模型切换配置项
    def on_model_change(e):
        config_container.controls.clear()
        if model_dropdown.value == "OpenAI":
            config_container.controls.extend([api_key_field, base_url_field])
        elif model_dropdown.value == "deepseek":
            config_container.controls.append(api_key_field)
        elif model_dropdown.value == "ollama":
            config_container.controls.append(addr_field)
        page.update()

    model_dropdown.on_change = on_model_change

    # 点击确认按钮
    def confirm_click(e):
        selected = model_dropdown.value
        msg = f"模型: {selected}\n"
        if selected == "OpenAI":
            msg += f"API Key: {api_key_field.value}\nBase URL: {base_url_field.value}"
        elif selected == "deepseek":
            msg += f"API Key: {api_key_field.value}"
        elif selected == "ollama":
            msg += f"服务地址: {addr_field.value}"

        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # 返回按钮点击
    def back_click(e):
        if on_back:
            on_back(page)  # 调用外部传入的返回函数
        else:
            page.snack_bar = ft.SnackBar(ft.Text("返回主页"))
            page.snack_bar.open = True
            page.update()

    # 初始加载时执行一次
    on_model_change(None)

    page.add(
        ft.Column(
            [

                model_dropdown,
                config_container,
                ft.ElevatedButton("确认", on_click=confirm_click),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )
