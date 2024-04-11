from dataclasses import KW_ONLY, dataclass, make_dataclass
from typing import Any, Generic, TypeVar

from turbobus.command import Command, CommandHandler, strict
from turbobus.injection import inject

from ..axioma.logger import ILogger

T = TypeVar('T')
X = TypeVar('X')

@dataclass(kw_only=True)
class LogCommand(Command[T], Generic[T]):

    content: T


@dataclass(kw_only=True)
class IntCommand(Command[str]):

    content: str

@inject(alias={ 'logger': 'ILogger2' })
@dataclass(kw_only=True)
class LogHandler(CommandHandler[LogCommand[T]]):
# class LogHandler(CommandHandler[IntCommand]):

    logger: ILogger

    def execute(self, x: LogCommand[T]) -> T:
    # def execute(self, x: IntCommand) -> str:
        # self.logger.print(x.content)
        return x.content

@inject(alias={ 'logger': 'ILogger' }, only=['logger'], exclude=['x'])
def test_dependency_injection_on_logger(logger: ILogger, x: int = 0):
    print('x', x)
    logger.print(': test_dependency_injection_on_logger')

@inject
def test_dependency_function_injection_on_logger(logger: ILogger):
    logger.print(': test_dependency_function_injection_on_logger')
