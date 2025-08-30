import sys
import io
import flet as ft


class CodeRunner(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.code_input = ft.TextField(
            label="请输入 Python 代码",
            multiline=True,
            expand=True,
            height=200,
            autofocus=True
        )
        self.output_box = ft.Text(value="", selectable=True)
        run_btn = ft.ElevatedButton("运行代码", on_click=self.run_code)

        self.controls.extend([
            self.code_input,
            run_btn,
            ft.Text("输出结果："),
            self.output_box
        ])

    def run_code(self, e=None):
        code = self.code_input.value
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()

        local_vars = {}
        result = None
        try:
            exec(code, {}, local_vars)
            last_line = code.strip().splitlines()[-1] if code.strip() else ""
            try:
                result = eval(last_line, {}, local_vars)
            except:
                result = None

            output = sys.stdout.getvalue()
            errors = sys.stderr.getvalue()
            output_text = ""
            if errors:
                output_text += f"错误:\n{errors}\n"
            if output:
                output_text += f"{output}\n"
            if result is not None:
                output_text += f"返回值: {result}"
            if not output_text.strip():
                output_text = "执行完成，无输出"

            self.output_box.value = output_text

        except Exception as ex:
            self.output_box.value = f"异常: {ex}"

        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr

        self.page.update()
