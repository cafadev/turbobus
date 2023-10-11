from abc import abstractmethod, ABC
from typing import Any, Generic, TypeAlias, TypeVar

CommandHandlerType: TypeAlias = 'CommandHandler'
HandlerType = TypeVar('HandlerType', bound=CommandHandlerType, covariant=True)
ReturnType = TypeVar('ReturnType')

class Command(ABC, Generic[HandlerType]):
    
    __handler__: type[HandlerType]


class CommandHandler(ABC, Generic[ReturnType, ]):

    def __init__(self, ) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, cmd: Command[HandlerType]) -> ReturnType:
        ...


class CommandBus:

    def execute(self, cmd, providers: dict[Any, Any] = {}):
        Handler = cmd.__handler__

        if Handler is None:
            from turbobus.exception import CommandHandlerDoesNotExistException
            raise CommandHandlerDoesNotExistException()

        result = Handler(**providers).execute(cmd)
        return result