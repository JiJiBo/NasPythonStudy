import os
import sys

def get_app_path():
    if getattr(sys, 'frozen', False):  # 如果是打包后的 exe
        app_dir = os.path.dirname(sys.executable)
    else:  # 运行 py 文件
        app_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(app_dir, 'db')
    return app_dir

app_path = get_app_path()
print("App 所在目录:", app_path)
