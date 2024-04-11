from abc import abstractmethod, ABC
from cgitb import handler
import inspect
from typing import Any, Callable, Generic, TypeVar, cast

from .exception import CommandHandlerDoesNotExistException
from turbobus.constants import Provider


ReturnType = TypeVar('ReturnType')


def strict(cls):
    function = cls.execute

    function_typing = list(function.__annotations__.values())

    if len(function_typing) < 2:
        return
    
    cmd, returnType = function_typing

    try:
        __return_type__ = cmd.__origin__.__return_type__
    except AttributeError:
        __return_type__ = cmd.__return_type__

    if cmd is not cls.__command__:
        raise TypeError(f"Incompatible command type - expected {cls.__command__} but got {cmd} in {cls.__name__}")

    if __return_type__ != returnType:
        raise TypeError(f"Incompatible return type - expected {cmd.__return_type__} but got {returnType} in {cls.__name__}")


class Command(Generic[ReturnType]):
    
    __return_type__: type[ReturnType]

    def __class_getitem__(cls, item):
        C = type(cls.__name__, (), { '__return_type__': item })
        return C


class CommandHandler(ABC, Generic[ReturnType]):

    __command__ = None

    def __class_getitem__(cls, item):
        C = type(cls.__name__, (cls, ), {
            '__command__': item,
            'execute': abstractmethod(lambda self, cmd: None)
        })

        return C
    
    def __init_subclass__(cls, *args, **kwargs):
        strict(cls)

    @abstractmethod
    def execute(self, cmd: Command[ReturnType]) -> ReturnType:
        """Execute method to implement the command logic"""


class CommandBus:

    def execute(self, cmd: Command[ReturnType], providers: dict[Any, Any] = {}) -> ReturnType:
        Handler = Provider.get(cmd.__class__.__name__)

        if Handler is None:
            raise CommandHandlerDoesNotExistException()

        handler = Handler(**providers)

        result = handler.execute(cmd)
        return cast(ReturnType, result)
