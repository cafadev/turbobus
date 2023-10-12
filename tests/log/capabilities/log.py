from dataclasses import dataclass
from turbobus.injection import inject
from turbobus.command import handler_of
from ..axioma.log import ILogHandler, ILogger, LogCommand


@handler_of(LogCommand)
@dataclass(kw_only=True)
class LogHandler(ILogHandler):

    dependency = inject(ILogger)

    def execute(self, cmd: LogCommand) -> str:
        self.dependency.logger(cmd.content)
        return cmd.content
