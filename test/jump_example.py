import flet as ft

def main(page: ft.Page):
    page.title = "Flet 页面跳转示例"

    # 定义页面1内容
    def page1():
        page.clean()  # 清空页面
        page.add(
            ft.Column(
                [
                    ft.Text("这是页面1"),
                    ft.ElevatedButton("跳转到页面2", on_click=lambda e: page2())
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    # 定义页面2内容
    def page2():
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("这是页面2"),
                    ft.ElevatedButton("返回页面1", on_click=lambda e: page1())
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    page1()  # 默认显示页面1

ft.app(target=main)
