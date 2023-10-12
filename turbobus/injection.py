from typing import TypeVar
from .constants import providers


T = TypeVar('T')


def injectable_of(to: type):
    def wrapper(cls):
        providers.__setitem__(to.__name__, cls)
        return cls

    return wrapper


def inject(cls: type[T]) -> T:
    Provider = providers.get(cls.__name__)

    assert Provider is not None

    return Provider()
