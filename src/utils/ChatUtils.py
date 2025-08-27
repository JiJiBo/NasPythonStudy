import json
import requests
from openai import OpenAI


class AIRequestHandler:
    """统一的 AI 请求处理类"""

    def __init__(
        self,
        provider="ollama",           # "ollama" | "openai" | "deepseek"
        model="deepseek-r1:14b",
        base_url="http://localhost:11434",
        api_key=None
    ):
        self.provider = provider
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "deepseek":
            self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
        else:
            self.client = None  # Ollama 用 requests 直接访问

    # ------------------ 流式 ------------------
    def stream_response(self, prompt, callback, error_callback=None):
        """
        流式获取AI回复
        Args:
            prompt: 用户输入
            callback: 每个片段的处理回调
            error_callback: 错误回调
        """
        try:
            if self.provider == "ollama":
                # 调用 Ollama 本地服务
                url = f"{self.base_url}/api/generate"
                payload = {"model": self.model, "prompt": prompt, "stream": True}
                with requests.post(url, json=payload, stream=True) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        if line:
                            chunk = json.loads(line.decode("utf-8"))
                            text = chunk.get("response", "")
                            if text:
                                callback(text)

            elif self.provider == "openai":
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        callback(delta.content)

            elif self.provider == "deepseek":
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True
                }
                with requests.post(self.deepseek_url, headers=headers, json=payload, stream=True) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        if line and line.startswith(b"data: "):
                            data = line[len(b"data: "):].decode("utf-8")
                            if data == "[DONE]":
                                break
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            if delta:
                                callback(delta)

        except Exception as e:
            if error_callback:
                error_callback(str(e))
            else:
                raise e

    # ------------------ 单次 ------------------
    def get_single_response(self, prompt):
        """
        获取单次完整回复（非流式）
        """
        try:
            if self.provider == "ollama":
                url = f"{self.base_url}/api/generate"
                payload = {"model": self.model, "prompt": prompt, "stream": False}
                resp = requests.post(url, json=payload)
                resp.raise_for_status()
                return resp.json().get("response", "")

            elif self.provider == "openai":
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return resp.choices[0].message.content

            elif self.provider == "deepseek":
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                }
                resp = requests.post(self.deepseek_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"错误: {str(e)}"
if __name__ == '__main__':
    # Ollama (本地 deepseek-r1:14b)
    ollama_ai = AIRequestHandler(provider="ollama", model="deepseek-r1:14b")
    print(ollama_ai.get_single_response("用python写一个冒泡排序"))


    # DeepSeek API
    deepseek_ai = AIRequestHandler(provider="deepseek", model="deepseek-chat", api_key="sk-你的Key")
    print(deepseek_ai.get_single_response("介绍一下强化学习"))
