from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from lib.utils.FontUtils import getFontSTX, getFontSTXName


class CodingApp(App):
    def build(self):
        LabelBase.register(
            name=getFontSTXName(),
            fn_regular=getFontSTX()
        )
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # 题目区域
        self.question = Label(
            text="题目：写一个函数，返回两个数的和。",
            size_hint=(1, 0.1), font_name="Chinese"
        )
        root.add_widget(self.question)

        # AI 提示区域
        self.ai_hint = Label(
            text="提示：你可以用 return a + b 来返回结果。",
            size_hint=(1, 0.1),
            color=(0, 0.5, 1, 1), font_name="Chinese"
        )
        root.add_widget(self.ai_hint)

        # 解题区域
        self.code_input = TextInput(
            hint_text="在这里输入你的代码...",
            multiline=True,
            size_hint=(1, 0.4), font_name="Chinese"
        )
        root.add_widget(self.code_input)

        # 按钮
        run_button = Button(
            text="运行代码",
            size_hint=(1, 0.1), font_name="Chinese"
        )
        run_button.bind(on_press=self.run_code)
        root.add_widget(run_button)

        # 结果区域
        self.result = Label(
            text="结果会显示在这里。",
            size_hint=(1, 0.2),
            color=(0.2, 0.7, 0.2, 1), font_name="Chinese"
        )
        root.add_widget(self.result)

        return root

    def run_code(self, instance):
        code = self.code_input.text

        try:
            # 运行用户代码
            local_vars = {}
            exec(code, {}, local_vars)

            if "add" in local_vars:  # 假设用户写了 add(a, b)
                test_result = local_vars["add"](2, 3)
                if test_result == 5:
                    self.result.text = "✅ 答对了！AI 点评：很好，你掌握了函数的写法！评分：90"
                else:
                    self.result.text = "❌ 答案不对，函数返回错误。评分：50"
            else:
                self.result.text = "⚠️ 你需要定义一个函数 add(a, b)"

        except Exception as e:
            self.result.text = f"运行错误：{e}"


if __name__ == "__main__":
    CodingApp().run()
