from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeAlias

from bus.bus import Command, CommandHandler
from bus.decorators import command


LogHandlerType: TypeAlias = "ILogHandler"

@dataclass
class LogCommand(Command[LogHandlerType]):

    content: str

class ILogHandler(CommandHandler[str]):

    ...

class ILogger(ABC):

    @abstractmethod
    def logger(self, text: str) -> None:
        ...