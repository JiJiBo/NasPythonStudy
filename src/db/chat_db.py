import json
import requests
import uuid
from openai import OpenAI
import sqlite3
from datetime import datetime
from src.db.llm_config_db import LLMConfigDB


class ChatDB:
    def __init__(self, db_path="chat.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute("""
                  CREATE TABLE IF NOT EXISTS chat
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      chat_id
                      TEXT,
                      role
                      TEXT,
                      content
                      TEXT,
                      timestamp
                      DATETIME
                      DEFAULT
                      CURRENT_TIMESTAMP
                  )
                  """)
        self.conn.commit()

    def save_message(self, chat_id, role, content):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO chat (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )
        self.conn.commit()

    def get_chat(self, chat_id):
        c = self.conn.cursor()
        c.execute(
            "SELECT id, role, content, timestamp FROM chat WHERE chat_id=? ORDER BY id",
            (chat_id,)
        )
        return c.fetchall()

    def delete_chat(self, chat_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM chat WHERE chat_id=?", (chat_id,))
        self.conn.commit()

    def get_recent_chat(self, chat_id, last_id=None, limit=100):
        """
        分页获取聊天记录
        :param chat_id: 聊天会话ID
        :param last_id: 从此id之后获取记录，如果为None则获取最新的limit条
        :param limit: 获取条数
        :return: list of records
        """
        c = self.conn.cursor()
        if last_id is None:
            # 获取最新的limit条
            c.execute(
                "SELECT id, role, content, timestamp FROM chat WHERE chat_id=? ORDER BY id DESC LIMIT ?",
                (chat_id, limit)
            )
            rows = c.fetchall()
            return rows[::-1]  # 逆序返回，保证时间顺序
        else:
            # 获取 id 之后的 limit 条
            c.execute(
                "SELECT id, role, content, timestamp FROM chat WHERE chat_id=? AND id>? ORDER BY id ASC LIMIT ?",
                (chat_id, last_id, limit)
            )
            return c.fetchall()

