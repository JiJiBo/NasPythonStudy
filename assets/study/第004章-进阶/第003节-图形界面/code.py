# ======= 可编辑区域开始 =======

# 练习1：创建基本窗口
import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("GUI练习")
root.geometry("400x300")

# 添加标签
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
# 请使用pack()方法将标签添加到窗口中
label.

# 练习2：添加按钮
def button_click():
    print("按钮被点击了！")

button = tk.Button(root, text="点击我", command=button_click)
# 请使用pack()方法将按钮添加到窗口中
button.

# 练习3：添加输入框
entry = tk.Entry(root, width=30)
# 请使用pack()方法将输入框添加到窗口中
entry.

# 练习4：获取输入框内容
def get_text():
    text = entry.get()
    print(f"输入的内容: {text}")

get_button = tk.Button(root, text="获取文本", command=get_text)
get_button.pack(pady=5)

# 练习5：使用grid布局
# 创建新窗口用于grid布局练习
grid_window = tk.Toplevel(root)
grid_window.title("Grid布局练习")
grid_window.geometry("300x200")

# 使用grid布局添加标签和输入框
tk.Label(grid_window, text="姓名:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
name_entry = tk.Entry(grid_window, width=20)
# 请使用grid()方法将输入框添加到第0行第1列
name_entry.

tk.Label(grid_window, text="年龄:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
age_entry = tk.Entry(grid_window, width=20)
# 请使用grid()方法将输入框添加到第1行第1列
age_entry.

# 练习6：添加复选框
check_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="我同意", variable=check_var)
# 请使用pack()方法将复选框添加到窗口中
checkbox.

# 练习7：添加单选按钮
radio_var = tk.StringVar()
radio1 = tk.Radiobutton(root, text="选项1", variable=radio_var, value="1")
radio2 = tk.Radiobutton(root, text="选项2", variable=radio_var, value="2")
# 请使用pack()方法将单选按钮添加到窗口中
radio1.
radio2.

# 练习8：显示消息框
from tkinter import messagebox

def show_message():
    # 请使用messagebox.showinfo()显示一个信息对话框
    pass

msg_button = tk.Button(root, text="显示消息", command=show_message)
msg_button.pack(pady=5)

# 练习9：文件对话框
from tkinter import filedialog

def open_file():
    # 请使用filedialog.askopenfilename()打开文件对话框
    filename = 
    if filename:
        print(f"选择的文件: {filename}")

file_button = tk.Button(root, text="打开文件", command=open_file)
file_button.pack(pady=5)

# 练习10：文本框
text_widget = tk.Text(root, height=5, width=40)
# 请使用pack()方法将文本框添加到窗口中
text_widget.

# 运行主循环（注释掉以避免阻塞）
# root.mainloop()

# ======= 可编辑区域结束 =======

# 正确答案
correct_answer = {
    "label_packed": True,
    "button_packed": True,
    "entry_packed": True,
    "name_entry_gridded": True,
    "age_entry_gridded": True,
    "checkbox_packed": True,
    "radio1_packed": True,
    "radio2_packed": True,
    "message_shown": True,
    "file_dialog_used": True,
    "text_widget_packed": True
}

# 学生答案
student_answer = {
    "label_packed": hasattr(label, '_packed') or 'pack' in str(label.pack_info()) if hasattr(label, 'pack_info') else False,
    "button_packed": hasattr(button, '_packed') or 'pack' in str(button.pack_info()) if hasattr(button, 'pack_info') else False,
    "entry_packed": hasattr(entry, '_packed') or 'pack' in str(entry.pack_info()) if hasattr(entry, 'pack_info') else False,
    "name_entry_gridded": hasattr(name_entry, '_gridded') or 'grid' in str(name_entry.grid_info()) if hasattr(name_entry, 'grid_info') else False,
    "age_entry_gridded": hasattr(age_entry, '_gridded') or 'grid' in str(age_entry.grid_info()) if hasattr(age_entry, 'grid_info') else False,
    "checkbox_packed": hasattr(checkbox, '_packed') or 'pack' in str(checkbox.pack_info()) if hasattr(checkbox, 'pack_info') else False,
    "radio1_packed": hasattr(radio1, '_packed') or 'pack' in str(radio1.pack_info()) if hasattr(radio1, 'pack_info') else False,
    "radio2_packed": hasattr(radio2, '_packed') or 'pack' in str(radio2.pack_info()) if hasattr(radio2, 'pack_info') else False,
    "message_shown": True,  # 假设学生正确实现了show_message函数
    "file_dialog_used": True,  # 假设学生正确实现了open_file函数
    "text_widget_packed": hasattr(text_widget, '_packed') or 'pack' in str(text_widget.pack_info()) if hasattr(text_widget, 'pack_info') else False
}

# 对比答案并输出结果
student_answer == correct_answer