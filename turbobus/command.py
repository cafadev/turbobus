from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast, dataclass_transform

from .exception import CommandHandlerDoesNotExist, IncompatibleCommandType, IncompatibleHandlerReturnType
from .constants import Provider


ReturnType = TypeVar('ReturnType')


@dataclass_transform(kw_only_default=True, frozen_default=True)
def kw_only_frozen(cls):
    C = dataclass(kw_only=True, frozen=True)(cls)
    return C


class Command(Generic[ReturnType]):
    
    __return_type__: type[ReturnType]

    def __class_getitem__(cls, returnType):
        

        C = type(cls.__name__, (), {
            '__return_type__': returnType,
        })

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
        function = cls.execute

        function_typing = list(function.__annotations__.values())

        if len(function_typing) < 2:
            return
        
        cmd, return_type = function_typing

        try:
            __return_type__ = cmd.__origin__.__return_type__
        except AttributeError:
            __return_type__ = cmd.__return_type__

        if cmd is not cls.__command__:
            raise IncompatibleCommandType(cls.__name__, cls.__command__, cmd)

        if __return_type__ != return_type:
            raise IncompatibleHandlerReturnType(cls.__name__, __return_type__, return_type)

    @abstractmethod
    def execute(self, cmd: Command[ReturnType]) -> ReturnType:
        """Execute method to implement the command logic"""


class CommandBus:

    def execute(self, cmd: Command[ReturnType], providers: dict[Any, Any] = {}) -> ReturnType:
        Handler = Provider.get(cmd.__class__.__name__)

        if Handler is None:
            raise CommandHandlerDoesNotExist()

        handler = Handler(**providers)

        result = handler.execute(cmd)
        return cast(ReturnType, result)
