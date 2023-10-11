from dataclasses import dataclass
from turbobus.decorators import command, injectable, injecting
from ..axioma.log import ILogger, LogCommand


@command(LogCommand)
@dataclass(kw_only=True)
class LogHandler:

    dependency = injecting(ILogger)

    def execute(self, cmd: LogCommand) -> str:
        if self.dependency is not None:
            self.dependency.logger(cmd.content)

        return cmd.content
