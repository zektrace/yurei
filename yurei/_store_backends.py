"""internal backends for kv storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any
import json
import sqlite3

_PRAGMA_JOURNAL_MODE = "WAL"
_PRAGMA_SYNCHRONOUS = "NORMAL"
_PRAGMA_CACHE_SIZE = -64000
_PRAGMA_TEMP_STORE = "MEMORY"


def _encode_value(value: Any) -> str:
    try:
        return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"value is not json-serializable: {exc}") from exc


def _decode_value(value: str) -> Any:
    return json.loads(value)


@dataclass(slots=True)
class InMemoryKVBackend:
    """in-memory backend for fast ephemeral storage."""

    data: dict[str, str] = field(default_factory=dict)
    lock: RLock = field(default_factory=RLock)

    def set(self, key: str, value: Any) -> None:
        payload = _encode_value(value)
        with self.lock:
            self.data[key] = payload

    def get(self, key: str, default: Any = None) -> Any:
        with self.lock:
            value = self.data.get(key)
        return default if value is None else _decode_value(value)

    def delete(self, key: str) -> bool:
        with self.lock:
            return self.data.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        with self.lock:
            return key in self.data

    def keys(self, prefix: str | None = None) -> list[str]:
        with self.lock:
            key_list = list(self.data.keys())
        if prefix:
            key_list = [k for k in key_list if k.startswith(prefix)]
        return sorted(key_list)

    def clear(self, prefix: str | None = None) -> int:
        with self.lock:
            if prefix is None:
                count = len(self.data)
                self.data.clear()
                return count

            keys_to_delete = [k for k in self.data if k.startswith(prefix)]
            for key in keys_to_delete:
                del self.data[key]
            return len(keys_to_delete)

    def close(self) -> None:
        return


@dataclass(slots=True)
class SQLiteKVBackend:
    """sqlite backend for persistent storage."""

    path: str
    conn: sqlite3.Connection = field(init=False)
    lock: RLock = field(default_factory=RLock)

    def __post_init__(self) -> None:
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.execute(f"PRAGMA journal_mode={_PRAGMA_JOURNAL_MODE}")
        self.conn.execute(f"PRAGMA synchronous={_PRAGMA_SYNCHRONOUS}")
        self.conn.execute(f"PRAGMA cache_size={_PRAGMA_CACHE_SIZE}")
        self.conn.execute(f"PRAGMA temp_store={_PRAGMA_TEMP_STORE}")
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kv (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def set(self, key: str, value: Any) -> None:
        payload = _encode_value(value)
        with self.lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)",
                (key, payload),
            )
            self.conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        with self.lock:
            row = self.conn.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
        return default if row is None else _decode_value(row[0])

    def delete(self, key: str) -> bool:
        with self.lock:
            cursor = self.conn.execute("DELETE FROM kv WHERE key=?", (key,))
            self.conn.commit()
            return cursor.rowcount > 0

    def exists(self, key: str) -> bool:
        with self.lock:
            row = self.conn.execute("SELECT 1 FROM kv WHERE key=? LIMIT 1", (key,)).fetchone()
        return row is not None

    def keys(self, prefix: str | None = None) -> list[str]:
        query = "SELECT key FROM kv ORDER BY key"
        params: tuple[str, ...] = ()
        if prefix:
            query = "SELECT key FROM kv WHERE key LIKE ? ORDER BY key"
            params = (f"{prefix}%",)

        with self.lock:
            rows = self.conn.execute(query, params).fetchall()
        return [row[0] for row in rows]

    def clear(self, prefix: str | None = None) -> int:
        query = "DELETE FROM kv"
        params: tuple[str, ...] = ()
        if prefix:
            query = "DELETE FROM kv WHERE key LIKE ?"
            params = (f"{prefix}%",)

        with self.lock:
            cursor = self.conn.execute(query, params)
            self.conn.commit()
            return cursor.rowcount

    def close(self) -> None:
        with self.lock:
            self.conn.close()
