import flet as ft
import re

from flet.core.container import Container
from flet.core.markdown import MarkdownCodeTheme, MarkdownExtensionSet, Markdown


class RichContent(ft.Column):
    def __init__(self, content: str = None, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 10
        self.controls = []
        self.expand = True
        self.text_str = ""
        if content:
            self.parse_and_add_content(content)

    def append(self, md_text: str):
        self.controls.clear()
        # 解析 think 标签
        # 按 <think> 切分
        import re

        # 使用非贪婪匹配，并处理可能不完整的情况
        parts = re.split(r"(<think>.*?</think>|<think>.*?$|^.*?</think>)", md_text, flags=re.DOTALL)

        for part in parts:
            if not part.strip():
                continue

            # 处理完整的 think 标签
            if part.startswith("<think>") and part.endswith("</think>"):
                think_text = part[len("<think>"):-len("</think>")].strip()
                if len(think_text) > 0:
                    self.controls.append(
                        ft.Container(
                            content=ft.Markdown(
                                "思考：" + think_text,
                                selectable=True,
                                code_theme=MarkdownCodeTheme.GOOGLE_CODE,
                                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=8,
                            padding=10,
                        )
                    )

            # 处理只有开始标签没有结束标签的情况
            elif part.startswith("<think>"):
                think_text = part[len("<think>"):].strip()
                if len(think_text) > 0:
                    self.controls.append(
                        ft.Container(
                            content=ft.Markdown(
                                "思考：" + think_text,
                                selectable=True,
                                code_theme=MarkdownCodeTheme.GOOGLE_CODE,
                                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=8,
                            padding=10,
                        )
                    )

            # 处理只有结束标签没有开始标签的情况
            elif part.endswith("</think>"):
                think_text = part[:-len("</think>")].strip()
                if len(think_text) > 0:
                    self.controls.append(
                        ft.Container(
                            content=ft.Markdown(
                                "思考：" + think_text,
                                selectable=True,
                                code_theme=MarkdownCodeTheme.GOOGLE_CODE,
                                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=8,
                            padding=10,
                        )
                    )

            # 处理普通文本
            else:
                self.controls.append(
                    ft.Markdown(
                        part,
                        selectable=True,
                        code_theme=MarkdownCodeTheme.GOOGLE_CODE,
                        extension_set=MarkdownExtensionSet.GITHUB_WEB,
                    )
                )

        if hasattr(self, 'page') and self.page:
            self.update()

    def parse_and_add_content(self, text: str):
        self.text_str += text
        
        # 使用防抖机制，避免频繁重新渲染
        if not hasattr(self, '_update_timer'):
            self._update_timer = None
        
        # 取消之前的定时器
        if self._update_timer:
            self._update_timer.cancel()
        
        # 设置新的定时器，100ms后更新UI
        import threading
        self._update_timer = threading.Timer(0.1, self._delayed_update)
        self._update_timer.start()
    
    def _delayed_update(self):
        """延迟更新UI，避免频繁重新渲染"""
        self.append(self.text_str)


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
