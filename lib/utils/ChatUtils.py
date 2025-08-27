import json

import requests


class AIRequestHandler:
    """AI请求处理类"""

    def __init__(self, base_url="http://localhost:11434", model="deepseek-r1:14b"):
        self.base_url = base_url
        self.model = model

    def stream_response(self, prompt, callback, error_callback=None):
        """
        流式获取AI回复

        Args:
            prompt: 用户输入的提示词
            callback: 处理每个响应片段的回调函数
            error_callback: 错误处理回调函数
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        try:
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        response_text = chunk.get("response", "")
                        if response_text:
                            callback(response_text)
        except Exception as e:
            if error_callback:
                error_callback(str(e))
            else:
                raise e

    def get_single_response(self, prompt):
        """
        获取单次完整回复（非流式）

        Args:
            prompt: 用户输入的提示词

        Returns:
            str: AI回复内容
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            return f"错误: {str(e)}"
