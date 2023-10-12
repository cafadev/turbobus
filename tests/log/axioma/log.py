from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeAlias

from turbobus.command import Command, CommandHandler


LogHandlerType: TypeAlias = "ILogHandler"

@dataclass
class LogCommand(Command[LogHandlerType]):

    content: str

class ILogHandler(CommandHandler[LogCommand, str]):

    ...

class ILogger(ABC):

    @abstractmethod
    def logger(self, text: str) -> None:
        ...
