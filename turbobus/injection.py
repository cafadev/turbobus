from typing import Any, Callable, get_type_hints
from .constants import providers

def __inject(dependency: str):
    if not isinstance(dependency, str):
        raise ValueError(f"Invalid dependency type {type(dependency)}")

    provider = providers.get(dependency)

    if provider is None:
        raise ValueError(f"Provider for {dependency} does not exist")

    return provider()


def inject(function: Callable[..., Any] | None = None) -> Any:
    # Check if dependency is type of function or class
    if function is not None:
        def wrapper(*args, **kwargs):
            hints = get_type_hints(function)
            injectable = { k: __inject(v.__name__) for k, v in hints.items() }

            return function(*args, **kwargs, **injectable)

        return wrapper

    if not isinstance(function, str):
        raise ValueError(f"Invalid dependency type {type(function)}") 

    return __inject(function)
