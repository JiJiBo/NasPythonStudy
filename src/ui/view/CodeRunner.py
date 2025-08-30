import sys
import io
import flet as ft


class CodeRunner(ft.Column):
    def __init__(self, page: ft.Page, codeReturn):
        super().__init__()
        self.page = page
        self.codeReturn = codeReturn
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

    def set_default_code(self, code):
        self.code_input.value = code

    def get_run_result(self):
        """
        执行当前输入框代码并返回结果字典：
        {
            "output": 控制台输出字符串,
            "error": 错误信息字符串,
            "return_value": eval 后的最后一行值
        }
        """
        code = self.code_input.value
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()

        local_vars = {}
        return_value = None
        output_text = ""
        error_text = ""

        try:
            exec(code, {}, local_vars)
            last_line = code.strip().splitlines()[-1] if code.strip() else ""
            try:
                return_value = eval(last_line, {}, local_vars)
            except:
                return_value = None

            output_text = sys.stdout.getvalue()
            error_text = sys.stderr.getvalue()

        except Exception as ex:
            error_text = str(ex)

        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
        if self.codeReturn is not None:
            result = return_value == self.codeReturn
            return {
                "错误信息": error_text.strip(),
                "执行结果": result,
                "代码": code,
                "期望输出": self.codeReturn,
                "执行输出": return_value
            }
        else:
            return {
                "错误信息": error_text.strip(),
                "代码": code,
                "执行输出": return_value,
                "期望输出": "",
            }
