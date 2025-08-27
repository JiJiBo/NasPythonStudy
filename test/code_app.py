import flet as ft
import re


class RichContent(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 10
        self.controls = []
        self.expand = True

    def add_markdown(self, md_text: str):
        self.controls.append(
            ft.Markdown(
                md_text,
                selectable=True,
                code_theme="monokai-sublime",
                extension_set="gitHubWeb",
                expand=True
            )
        )
        if self.page:
            self.update()

    def add_latex(self, latex: str):
        md_content = f"$$\n{latex}\n$$"
        self.add_markdown(md_content)

    def add_code(self, code: str, language="python"):
        md_code = f"```{language}\n{code}\n```"
        self.add_markdown(md_code)

    def parse_and_add_content(self, text: str):
        # 分割文本块
        blocks = re.split(r'\n\s*\n', text)

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            # 检测LaTeX公式 (包含$$的块)
            if re.match(r'^\$\$[\s\S]*\$\$$', block):
                latex = re.sub(r'^\$\$(.*)\$\$$', r'\1', block, flags=re.DOTALL)
                self.add_latex(latex)

            # 检测代码块 (包含```的块)
            elif re.match(r'^```.*\n[\s\S]*\n```$', block):
                match = re.match(r'^```(\w*)\n([\s\S]*)\n```$', block)
                language = match.group(1) if match.group(1) else "text"
                code = match.group(2)
                self.add_code(code, language)

            # 否则作为Markdown处理
            else:
                self.add_markdown(block)

