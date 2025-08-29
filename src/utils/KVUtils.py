import os
import json
from typing import Any

class KVUtils:
    def __init__(self, path: str = "kv_store.json"):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    # ---------- 基础方法 ----------
    def put(self, key: str, value: Any):
        """存储任意值（自动推断类型）"""
        if isinstance(value, (int, float, bool, str)):
            self._data[key] = value
            self._save()
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    # ---------- 类型安全方法 ----------
    def put_int(self, key: str, value: int):
        if not isinstance(value, int):
            raise TypeError("Value must be int")
        self.put(key, value)

    def get_int(self, key: str, default: int = 0) -> int:
        return int(self._data.get(key, default))

    def put_float(self, key: str, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError("Value must be float")
        self.put(key, float(value))

    def get_float(self, key: str, default: float = 0.0) -> float:
        return float(self._data.get(key, default))

    def put_bool(self, key: str, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Value must be bool")
        self.put(key, value)

    def get_bool(self, key: str, default: bool = False) -> bool:
        return bool(self._data.get(key, default))

    def put_str(self, key: str, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must be str")
        self.put(key, value)

    def get_str(self, key: str, default: str = "") -> str:
        return str(self._data.get(key, default))

    # ---------- 工具方法 ----------
    def remove(self, key: str):
        if key in self._data:
            del self._data[key]
            self._save()

    def clear(self):
        self._data.clear()
        self._save()
