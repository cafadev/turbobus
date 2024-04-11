from typing import Any, Callable, get_type_hints
from .constants import Provider


def __inject(dependency: str):
    if not isinstance(dependency, str):
        raise ValueError(f"Invalid dependency type {type(dependency)}")

    provider = Provider.get(dependency)

    if provider is None:
        raise ValueError(f"Provider for {dependency} does not exist")

    return provider()


def inject(function: Callable[..., Any] | None = None, /, *, alias: dict[str, str] | None = None,
           exclude: list[str] = [], only: list[str] = []) -> Any:
    # Check if dependency is type of function or class
    if function is not None:
        def wrapper(*args, **kwargs):
            hints = get_type_hints(function)
            
            if alias:
                hints: dict[str, Any] = { k: alias.get(k, v) for k, v in hints.items() }

            injectable = { k: __inject(v.__name__ if type(v) is not str else v) for k, v in hints.items() }

            return function(*args, **kwargs, **injectable)

        return wrapper
    
    def decorator(function: Callable[..., Any]) -> Any:
        def wrapper(*args, **kwargs):
            hints = get_type_hints(function)

            # exclude keys from hints using exclude list parameter
            if exclude:
                hints = { k: v for k, v in hints.items() if k not in exclude }

            # only keys from hints using only list parameter
            if only:
                hints = { k: v for k, v in hints.items() if k in only }
            
            if alias is not None:
                hints: dict[str, Any] = { k: alias.get(k, v) for k, v in hints.items() }

            injectable = { k: __inject(v.__name__ if type(v) is not str else v) for k, v in hints.items() }

            return function(*args, **kwargs, **injectable)

        return wrapper
    
    return decorator
