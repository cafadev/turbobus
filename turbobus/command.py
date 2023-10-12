from abc import abstractmethod, ABC
from typing import Generic, TypeAlias, TypeVar
from .constants import providers

CommandHandlerType: TypeAlias = 'CommandHandler'
HandlerType = TypeVar('HandlerType', bound=CommandHandlerType, covariant=True)
ReturnType = TypeVar('ReturnType')

class Command(ABC, Generic[HandlerType]):
    
    __handler__: type[HandlerType]


CommandType = TypeVar('CommandType', bound=Command)
class CommandHandler(ABC, Generic[CommandType, ReturnType]):

    def __init__(self, ) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, cmd: CommandType) -> ReturnType:
        ...


def handler_of(commandClass, injectable: type | None = None):
    def wrapper(handlerClass):
        if injectable is not None:
            providers.__setitem__(injectable.__name__, handlerClass)

        commandClass.__handler__ = handlerClass
        return handlerClass

    return wrapper
