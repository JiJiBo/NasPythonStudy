# 调用模块
import requests
import json

def deepseek_chat(prompt, model):
    # # deepseek的API接口链接
    url = "http://localhost:11434/api/generate"
    # 基本请求参数
    payload = {
        "model": model,  # 调用的AI模型
        "prompt": prompt,  # 输入的对话文本或指令
        "stream": True  # 启用流式响应
    }
    # 向Deepseek模型的API接口发起请求，并实时显示回复信息
    with requests.post(url, json=payload, stream=True) as res:
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                print(chunk.get("response",""),end="", flush=True)

# 1、向AI进行提问，写出需要询问的问题
prompt = "如何学习Python编程？"
# 2、需要调用的AI模型，根据本地下载的模型，写入模型名称即可
model = 'deepseek-r1:14b'
# 3、调用函数，与Deepseek建立响应
deepseek_chat(prompt,model)
