from dataclasses import KW_ONLY, dataclass, make_dataclass
from typing import Any, TypeVar, cast

from turbobus.command import Command, CommandHandler, strict
from turbobus.injection import inject

from ..axioma.logger import ILogger

T = TypeVar('T')
X = TypeVar('X')

@dataclass(kw_only=True)
class LogCommand(Command[str]):

    content: str


@dataclass(kw_only=True)
class IntCommand(Command[int]):

    content: str

@inject
@dataclass(kw_only=True)
class LogHandler(CommandHandler[LogCommand]):

    logger: ILogger

    def execute(self, x: LogCommand) -> str:
        self.logger.print(x.content)
        return x.content

@inject
def test_dependency_injection_on_logger(logger: ILogger):
    logger.print(': test_dependency_injection_on_logger')

@inject
def test_dependency_function_injection_on_logger(logger: ILogger):
    logger.print(': test_dependency_function_injection_on_logger')
