from typing import TypeVar


providers = {}
T = TypeVar('T')


def command(commandClass, injectable: type | None = None):

    def wrapper(handlerClass):
        if injectable is not None:
            providers.__setitem__(injectable.__name__, handlerClass)

        commandClass.__handler__ = handlerClass
        return handlerClass

    return wrapper


def injectable(to: type):
    def wrapper(cls):
        providers.__setitem__(to.__name__, cls)
        return cls

    return wrapper


def injecting(cls: type[T]) -> T:
    Provider = providers.get(cls.__name__)

    assert Provider is not None

    return Provider()
