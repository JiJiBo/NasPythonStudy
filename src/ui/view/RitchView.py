import flet as ft

from flet.core.markdown import MarkdownCodeTheme, MarkdownExtensionSet


class RichContent(ft.Column):
    def __init__(self, content: str = None, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 10
        self.controls = []
        self.expand = True

        # 如果构造器传入内容，直接解析并添加
        if content:
            self.parse_and_add_content(content)

    def append(self, md_text: str):
        md_value=""
        if len(self.controls) != 0:
            for control in self.controls:
                md_value += control.value
        self.controls.clear()
        self.controls.append(
            ft.Markdown(
                md_value+md_text,
                selectable=True,
                code_theme=MarkdownCodeTheme.GOOGLE_CODE,
                extension_set=MarkdownExtensionSet.GITHUB_WEB,
            )
        )
        if hasattr(self, 'page') and self.page:
            self.update()

    def parse_and_add_content(self, text: str):
        self.append(text)


def main(page: ft.Page):
    page.title = "RichContent Markdown 预览"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    # 示例 Markdown 内容
    md_text = """
# 这是一个标题

这是普通文本，可以复制。

## 代码示例

```python
def hello():
    print("Hello World")
```
    """
    rich_content = RichContent(md_text)
    page.add(rich_content)


if __name__ == '__main__':
    ft.app(target=main)
