from typing import Any, TypeVar

from .exception import CommandHandlerDoesNotExistException

ReturnType = TypeVar('ReturnType')

class CommandBus:

    def execute(self, cmd, providers: dict[Any, Any] = {}):
        Handler = cmd.__handler__

        if Handler is None:
            raise CommandHandlerDoesNotExistException()

        result = Handler(**providers).execute(cmd)
        return result