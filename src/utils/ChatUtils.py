import json
import requests
from openai import OpenAI

from src.db.chat_db import ChatDB
from src.db.llm_config_db import LLMConfigDB
from src.utils.LocalLLMEngine import local_llm_engine


class AIRequestHandlerWithHistory:
    def __init__(self):
        self.handler = AIRequestHandler.from_current_config()
        self.db = ChatDB()
        self._cancelled = False

    def refresh_config(self):
        self.handler.refresh_config()

    def cancel_current_request(self):
        """取消当前正在进行的请求"""
        self._cancelled = True

    def reset_cancel_flag(self):
        """重置取消标志"""
        self._cancelled = False

    def is_cancelled(self):
        """检查是否已取消"""
        return self._cancelled

    # ---------------- 工具方法 ----------------
    def build_prompt_with_history(self, chat_id, new_prompt, n=20):
        """
        组装前 n 条历史 + 当前输入，返回 messages 格式
        """
        history = self.db.get_recent_chat(chat_id, limit=n)
        messages = []
        for record in history:
            msg_id, role, content, *_ = record
            if role == "user":
                messages.append({"role": "user", "content": content})
            elif role == "assistant":
                messages.append({"role": "assistant", "content": content})

        messages.append({"role": "user", "content": new_prompt})
        return messages

    # ---------------- 单次请求 ----------------
    def get_single_response(self, chat_id, prompt, n=20):
        if not self.handler.valid:
            return None, "当前没有配置 LLM，请先到设置页面添加或选择配置。"

        # 先保存用户消息
        self.db.save_message(chat_id, "user", prompt)
        
        # 构建消息（包含历史记录作为记忆）
        messages = self.build_prompt_with_history(chat_id, prompt, n)
        
        resp = self.handler.get_response_with_history(messages)
        
        # 保存AI响应
        self.db.save_message(chat_id, "assistant", resp)
        return chat_id, resp

    # ---------------- 流式请求 ----------------
    def send_message(self, chat_id, prompt, callback=None, error_callback=None, n=20):
        if not self.handler.valid:
            if callback:
                callback("当前没有配置 LLM，请先到设置页面添加或选择配置。")
            return None

        # 重置取消标志，开始新请求
        self.reset_cancel_flag()

        # 先保存用户消息
        self.db.save_message(chat_id, "user", prompt)
        
        full_response = ""

        def inner_callback(text):
            nonlocal full_response
            # 检查是否已取消
            if self.is_cancelled():
                return
            full_response += text
            if callback:
                callback(text)

        def inner_error_callback(err):
            # 检查是否已取消，如果是取消导致的错误则不处理
            if not self.is_cancelled() and error_callback:
                error_callback(err)

        # 构建消息（包含历史记录作为记忆）
        messages = self.build_prompt_with_history(chat_id, prompt, n)

        self.handler.stream_response_with_history(
            messages,
            callback=inner_callback,
            error_callback=inner_error_callback,
            cancel_check=self.is_cancelled
        )

        # 如果没有被取消，保存AI响应
        if not self.is_cancelled():
            self.db.save_message(chat_id, "assistant", full_response)
        return chat_id

    # ---------------- 历史记录 ----------------
    def get_chat_history(self, chat_id):
        return self.db.get_chat(chat_id)

    def delete_chat_history(self, chat_id):
        self.db.delete_chat(chat_id)
    
    def clean_contaminated_messages(self, chat_id):
        """清理被污染的消息（包含user/assistant标签的消息）"""
        history = self.db.get_chat(chat_id)
        cleaned_count = 0
        
        for record in history:
            msg_id, role, content, timestamp = record
            # 检查是否包含污染标签
            if role == "assistant" and ("user\n" in content or "assistant\n" in content or "User:" in content or "Assistant:" in content):
                # 删除这条被污染的消息
                c = self.db.conn.cursor()
                c.execute("DELETE FROM chat WHERE id=?", (msg_id,))
                self.db.conn.commit()
                cleaned_count += 1
                print(f"清理被污染的消息: {content[:50]}...")
        
        if cleaned_count > 0:
            print(f"已清理 {cleaned_count} 条被污染的消息")
        return cleaned_count
    
    def force_clean_all_assistant_messages(self, chat_id):
        """强制清理所有assistant消息（用于严重污染的情况）"""
        c = self.db.conn.cursor()
        c.execute("DELETE FROM chat WHERE chat_id=? AND role='assistant'", (chat_id,))
        deleted_count = c.rowcount
        self.db.conn.commit()
        print(f"已强制清理 {deleted_count} 条assistant消息")
        return deleted_count

    def get_recent_history(self, chat_id, last_id=None, limit=20):
        return self.db.get_recent_chat(chat_id, last_id=last_id, limit=limit)

    def get_last_message_id(self, chat_id):
        history = self.db.get_recent_chat(chat_id, limit=1)
        if history:
            return history[-1][0]
        return None


class AIRequestHandler:
    def __init__(self, provider=None, model=None, base_url=None, api_key=None, valid=True):
        self.provider = provider
        self.model = model or "deepseek-r1:14b"
        self.base_url = base_url.rstrip("/") if base_url else None
        self.api_key = api_key
        self.valid = valid

        self._init_client()

    def _init_client(self):
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
        elif self.provider.lower() == "local_model":
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
        elif provider == "local_model":
            return cls(
                provider=config.get("provider"),
                model=config.get("model"),
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                valid=True
            )

    def refresh_config(self):
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
        elif provider == "local_model":
            self.base_url = None  # 本地模型不需要base_url
        self._init_client()

    # ---------------- 单次响应（带历史） ----------------
    def get_response_with_history(self, messages):
        try:
            if self.provider == "ollama":
                url = f"{self.base_url}/api/chat"
                payload = {"model": self.model, "messages": messages, "stream": False}
                resp = requests.post(url, json=payload)
                resp.raise_for_status()
                return resp.json().get("message", {}).get("content", "")

            elif self.provider == "openai":
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return resp.choices[0].message.content

            elif self.provider == "deepseek":
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {"model": self.model, "messages": messages, "stream": False}
                resp = requests.post(self.deepseek_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]

            elif self.provider == "local_model":
                # 使用本地模型引擎
                if not local_llm_engine.is_loaded:
                    # 尝试加载模型
                    if not local_llm_engine.load_model(self.model):
                        return "错误: 无法加载本地模型"
                
                return local_llm_engine.generate_response(messages)

        except Exception as e:
            return f"错误: {str(e)}"

    # ---------------- 流式响应（带历史） ----------------
    def stream_response_with_history(self, messages, callback, error_callback=None, cancel_check=None):
        try:
            if self.provider == "ollama":
                url = f"{self.base_url}/api/chat"
                payload = {"model": self.model, "messages": messages, "stream": True}
                with requests.post(url, json=payload, stream=True) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        # 检查是否需要取消
                        if cancel_check and cancel_check():
                            break
                        if line:
                            chunk = json.loads(line.decode("utf-8"))
                            text = chunk.get("message", {}).get("content", "")
                            if text:
                                callback(text)

            elif self.provider == "openai":
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True
                )
                for chunk in stream:
                    # 检查是否需要取消
                    if cancel_check and cancel_check():
                        break
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        callback(delta.content)

            elif self.provider == "deepseek":
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {"model": self.model, "messages": messages, "stream": True}
                with requests.post(self.deepseek_url, headers=headers, json=payload, stream=True) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        # 检查是否需要取消
                        if cancel_check and cancel_check():
                            break
                        if line and line.startswith(b"data: "):
                            data = line[len(b"data: "):].decode("utf-8")
                            if data == "[DONE]":
                                break
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            if delta:
                                callback(delta)

            elif self.provider == "local_model":
                # 使用本地模型引擎进行流式响应
                if not local_llm_engine.is_loaded:
                    # 尝试加载模型
                    if not local_llm_engine.load_model(self.model):
                        if error_callback:
                            error_callback("错误: 无法加载本地模型")
                        return
                
                local_llm_engine.stream_response(
                    messages, 
                    callback=callback, 
                    error_callback=error_callback,
                    cancel_check=cancel_check
                )

        except Exception as e:
            if error_callback:
                error_callback(str(e))
            else:
                raise e


