import os
import json
import csv
import pickle
import sqlite3
from typing import Any, List, Dict

class SPUtils:
    """数据存取工具类"""

    # ---------- JSON ----------
    @staticmethod
    def save_json(data: Any, path: str, indent: int = 4):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

    @staticmethod
    def load_json(path: str) -> Any:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------- CSV ----------
    @staticmethod
    def save_csv(data: List[Dict[str, Any]], path: str):
        if not data:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def load_csv(path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # ---------- Pickle ----------
    @staticmethod
    def save_pickle(data: Any, path: str):
        with open(path, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def load_pickle(path: str) -> Any:
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return pickle.load(f)

    # ---------- SQLite ----------
    @staticmethod
    def init_sqlite(path: str, table: str, schema: str):
        """
        初始化数据库
        schema 示例: "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        """
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
        conn.commit()
        conn.close()

    @staticmethod
    def insert_sqlite(path: str, table: str, data: Dict[str, Any]):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        keys = ",".join(data.keys())
        placeholders = ",".join("?" * len(data))
        c.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", tuple(data.values()))
        conn.commit()
        conn.close()

    @staticmethod
    def query_sqlite(path: str, table: str, where: str = "") -> List[Dict[str, Any]]:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sql = f"SELECT * FROM {table} {('WHERE ' + where) if where else ''}"
        rows = c.execute(sql).fetchall()
        conn.close()
        return [dict(row) for row in rows]
