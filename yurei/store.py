"""simple kv store with pluggable backends."""

from __future__ import annotations

from typing import Any

from ._store_backends import InMemoryKVBackend, SQLiteKVBackend


class KVStore:
    """minimal key-value store backed by sqlite or memory."""

    def __init__(self, path: str | None = None) -> None:
        self.path = path
        if path:
            self._backend = SQLiteKVBackend(path)
        else:
            self._backend = InMemoryKVBackend()

    def set(self, key: str, value: Any) -> None:
        """store a value under a key."""
        if not key:
            raise ValueError("key cannot be empty")
        self._backend.set(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """read a value from storage."""
        if not key:
            return default
        return self._backend.get(key, default)

    def delete(self, key: str) -> bool:
        """remove a key if present."""
        if not key:
            return False
        return self._backend.delete(key)

    def exists(self, key: str) -> bool:
        """check key existence without loading the value."""
        if not key:
            return False
        return self._backend.exists(key)

    def keys(self, prefix: str | None = None) -> list[str]:
        """list sorted keys, optionally filtered by prefix."""
        return self._backend.keys(prefix)

    def clear(self, prefix: str | None = None) -> int:
        """delete all keys or all keys under a prefix."""
        return self._backend.clear(prefix)

    def close(self) -> None:
        """close any open resources."""
        self._backend.close()

    def __enter__(self) -> "KVStore":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False

    def __del__(self) -> None:
        self.close()
