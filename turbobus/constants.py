from typing import Any


class Provider:

    providers: dict[str, Any] = {}

    @classmethod
    def set(cls, key: str, value: Any):
        cls.providers[key] = value

    @classmethod
    def get(cls, key: str) -> Any:
        return cls.providers.get(key)