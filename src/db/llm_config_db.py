import sqlite3
import os

class LLMConfigDB:
    def __init__(self, db_path="llm_config.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # 模型配置表
        c.execute("""
            CREATE TABLE IF NOT EXISTS llm_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                model TEXT,
                base_url TEXT,
                api_key TEXT,
                addr TEXT
            )
        """)

        # 当前启用的配置
        c.execute("""
            CREATE TABLE IF NOT EXISTS llm_current (
                id INTEGER PRIMARY KEY CHECK (id=1),
                config_id INTEGER,
                FOREIGN KEY(config_id) REFERENCES llm_config(id)
            )
        """)

        # 确保有一行默认 current
        c.execute("INSERT OR IGNORE INTO llm_current (id, config_id) VALUES (1, NULL)")

        conn.commit()
        conn.close()

    # 保存/更新配置（返回配置id）
    def save_config(self, provider, model=None, base_url=None, api_key=None, addr=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # 先删除已有相同 provider 的配置
        c.execute("DELETE FROM llm_config WHERE provider = ?", (provider,))

        # 插入新配置
        c.execute("""
                  INSERT INTO llm_config (provider, model, base_url, api_key, addr)
                  VALUES (?, ?, ?, ?, ?)
                  """, (provider, model, base_url, api_key, addr))

        config_id = c.lastrowid
        conn.commit()
        conn.close()
        return config_id

    # 获取所有配置
    def get_all_configs(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, provider, model, base_url, api_key, addr FROM llm_config")
        rows = c.fetchall()
        conn.close()
        return [
            {"id": r[0], "provider": r[1], "model": r[2], "base_url": r[3], "api_key": r[4], "addr": r[5]}
            for r in rows
        ]

    # 设置当前 provider
    def set_current_config(self, config_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE llm_current SET config_id=? WHERE id=1", (config_id,))
        conn.commit()
        conn.close()

    # 获取当前配置
    def get_current_config(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            SELECT llm_config.id, provider, model, base_url, api_key, addr
            FROM llm_current
            LEFT JOIN llm_config ON llm_current.config_id = llm_config.id
            WHERE llm_current.id=1
        """)
        row = c.fetchone()
        conn.close()
        if row and row[0]:
            return {"id": row[0], "provider": row[1], "model": row[2], "base_url": row[3], "api_key": row[4], "addr": row[5]}
        return None
    # 根据模型类型获取最新配置（按 id 降序，取最新一条）
    def get_latest_config_by_model(self, model_type):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            SELECT id, provider, model, base_url, api_key, addr
            FROM llm_config
            WHERE provider=? 
            ORDER BY id DESC
            LIMIT 1
        """, (model_type,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "provider": row[1],
                "model": row[2],
                "base_url": row[3],
                "api_key": row[4],
                "addr": row[5],
            }
        return None
    def delete_config(self, config_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # 先检查是否是当前选中配置，如果是，则清空 current
        c.execute("SELECT config_id FROM llm_current WHERE id=1")
        current = c.fetchone()
        if current and current[0] == config_id:
            c.execute("UPDATE llm_current SET config_id=NULL WHERE id=1")

        # 删除配置
        c.execute("DELETE FROM llm_config WHERE id=?", (config_id,))
        conn.commit()
        conn.close()