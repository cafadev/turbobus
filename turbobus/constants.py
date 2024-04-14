from typing import Any


class Provider:

    _providers: dict[str, Any] = {}

    @classmethod
    def set(cls, key: type | str, value: Any):
        provider_name = key if isinstance(key, str) else key.__name__
        cls._providers[provider_name] = value

    @classmethod
    def get(cls, key: type | str) -> Any:
        return cls._providers.get(key if isinstance(key, str) else key.__name__)
    
    @classmethod
    def clear(cls):
        cls._providers = {}