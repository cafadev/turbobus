from dataclasses import dataclass

from typing import TypeVar
from turbobus import command
from turbobus.command import Command, CommandHandler
from turbobus.injection import inject

from ..axioma.logger import ILogger

T = TypeVar('T')
X = TypeVar('X')

@command
class LogCommand(Command[str]):

    content: str

@dataclass(kw_only=True)
class IntCommand(Command[str]):

    content: str

@inject
@dataclass(kw_only=True)
class LogHandler(CommandHandler[LogCommand]):
# class LogHandler(CommandHandler[IntCommand]):

    logger: ILogger

    # def execute(self, x: LogCommand[T]) -> T:
    def execute(self, x: LogCommand) -> str:
        self.logger.print(x.content)
        return x.content

@inject(alias={ 'logger': 'ILogger' }, only=['logger'], exclude=['x'])
def test_dependency_injection_on_logger(logger: ILogger, x: int = 0):
    print('x', x)
    logger.print(': test_dependency_injection_on_logger')

@inject
def test_dependency_function_injection_on_logger(logger: ILogger):
    logger.print(': test_dependency_function_injection_on_logger')
