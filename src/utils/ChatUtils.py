import json

import requests
from openai import OpenAI

from src.db.llm_config_db import LLMConfigDB


class AIRequestHandler:
    """统一的 AI 请求处理类"""

    def __init__(
            self,
            provider=None,
            model=None,
            base_url=None,
            api_key=None,
            valid=True,  # 是否有效配置
    ):
        self.provider = provider
        self.model = model or "deepseek-r1:14b"
        self.base_url = base_url.rstrip("/") if base_url else None
        self.api_key = api_key
        self.valid = valid

        self._init_client()

    def _init_client(self):
        """初始化 client"""
        if not self.valid:
            self.client = None
            return

        if self.provider.lower() == "openai":
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        elif self.provider.lower() == "deepseek":
            self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
            self.client = None
        elif self.provider.lower() == "ollama":
            self.client = None
        else:
            self.client = None

    @classmethod
    def from_current_config(cls):
        db = LLMConfigDB()
        config = db.get_current_config()
        if not config:
            return cls(valid=False)
        provider = config.get("provider")
        if provider == "openai":
            return cls(
                provider=config.get("provider"),
                model=config.get("model"),
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                valid=True
            )
        elif provider == "deepseek":
            return cls(
                provider=config.get("provider"),
                model=config.get("model"),
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                valid=True
            )
        elif provider == "ollama":
            return cls(
                provider=config.get("provider"),
                model=config.get("model"),
                base_url=config.get("addr"),
                api_key=config.get("api_key"),
                valid=True
            )

    def refresh_config(self):
        """刷新当前数据库配置"""
        db = LLMConfigDB()
        config = db.get_current_config()
        if not config:
            self.valid = False
            self.provider = None
            self.model = None
            self.base_url = None
            self.api_key = None
            self.client = None
            return

        self.provider = config.get("provider")
        self.model = config.get("model") or "deepseek-r1:14b"

        self.api_key = config.get("api_key")
        self.valid = True
        provider = config.get("provider")
        if provider == "openai":
            self.base_url = config.get("base_url").rstrip("/") if config.get("base_url") else None
        elif provider == "deepseek":

            self.base_url = config.get("base_url").rstrip("/") if config.get("base_url") else None
        elif provider == "ollama":
            self.base_url = config.get("addr").rstrip("/") if config.get("addr") else None
        self._init_client()

    # ------------------ 单次 ------------------
    def get_single_response(self, prompt):
        if not self.valid:
            return "当前没有配置 LLM，请先到设置页面添加或选择配置。"

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

    # ------------------ 流式 ------------------
    def stream_response(self, prompt, callback, error_callback=None):
        if not self.valid:
            callback("当前没有配置 LLM，请先到设置页面添加或选择配置。")
            return
        try:
            if self.provider == "ollama":
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
        if not self.valid:
            return "当前没有配置 LLM，请先到设置页面添加或选择配置。"

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


ai_handler = AIRequestHandler.from_current_config()
if __name__ == '__main__':
    # 使用当前配置
    ai = AIRequestHandler.from_current_config()
    print(ai.get_single_response("用python写一个冒泡排序"))
