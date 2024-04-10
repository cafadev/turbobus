from tests.log.capabilities.log import LogCommand, LogHandler
from turbobus.constants import providers

from tests.log.axioma.logger import ILogger
from tests.log.capabilities.logger import Logger

providers[ILogger.__name__] = Logger
providers[LogCommand.__name__] = LogHandler
