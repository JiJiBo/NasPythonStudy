import sqlite3
import os
import sys

from src.db.path_utils import get_app_path


class LocalDB:
    def __init__(self, db_name="app_data.db", tables=None):
        """
        初始化本地 SQLite 数据库
        :param db_name: 数据库文件名
        :param tables: 表定义字典，格式：
            {
                "users": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL",
                "products": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL"
            }
        """
        self.db_path = os.path.join(get_app_path(), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.tables = tables or {}
        self._init_tables()

    def _init_tables(self):
        """初始化表"""
        for table_name, schema in self.tables.items():
            # IF NOT EXISTS 避免多次初始化重复创建表
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
            self.cursor.execute(sql)
        self.conn.commit()

    # ------------------- CRUD 操作 -------------------
    def add(self, table, **kwargs):
        """增加一条记录"""
        keys = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        values = tuple(kwargs.values())
        sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all(self, table):
        """获取表中所有记录"""
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    def get_by_id(self, table, record_id):
        """根据 ID 获取单条记录"""
        self.cursor.execute(f"SELECT * FROM {table} WHERE id=?", (record_id,))
        return self.cursor.fetchone()

    def update(self, table, record_id, **kwargs):
        """更新记录"""
        set_str = ", ".join([f"{k}=?" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (record_id,)
        sql = f"UPDATE {table} SET {set_str} WHERE id=?"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete(self, table, record_id):
        """删除记录"""
        self.cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
        self.conn.commit()

    def close(self):
        """关闭数据库"""
        self.conn.close()


# ------------------- 使用示例 -------------------
if __name__ == "__main__":
    tables = {
        "users": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL"
    }

    db = LocalDB(tables=tables)

    # 增加记录
    uid = db.add("users", name="Alice", age=25)
    print("添加记录 ID:", uid)

    # 查询所有
    print("所有用户:", db.get_all("users"))

    # 修改记录
    db.update("users", uid, name="Alice Zhang", age=26)
    print("修改后:", db.get_by_id("users", uid))

    # 删除记录
    db.delete("users", uid)
    print("删除后:", db.get_all("users"))

    db.close()
