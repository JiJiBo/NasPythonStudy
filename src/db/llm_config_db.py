import sqlite3
import os

class LLMConfigDB:
    def __init__(self, db_path="llm_config.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_type TEXT NOT NULL,
                api_key TEXT,
                base_url TEXT,
                addr TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def save_config(self, model_type, api_key=None, base_url=None, addr=None):
        """新增一条配置"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO llm_config (model_type, api_key, base_url, addr) VALUES (?, ?, ?, ?)",
            (model_type, api_key, base_url, addr),
        )
        conn.commit()
        conn.close()

    def load_all_configs(self):
        """加载所有配置"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, model_type, api_key, base_url, addr FROM llm_config")
        rows = cursor.fetchall()
        conn.close()
        return [
            {"id": r[0], "model_type": r[1], "api_key": r[2], "base_url": r[3], "addr": r[4]}
            for r in rows
        ]

    def delete_config(self, config_id):
        """删除某个配置"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM llm_config WHERE id=?", (config_id,))
        conn.commit()
        conn.close()
