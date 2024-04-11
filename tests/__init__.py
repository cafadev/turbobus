from tests.log.capabilities.log import LogCommand, LogHandler
from turbobus.constants import Provider

from tests.log.axioma.logger import ILogger
from tests.log.capabilities.logger import Logger, Logger2


Provider.set(ILogger.__name__, Logger)
Provider.set('ILogger2', Logger2)
Provider.set(LogCommand.__name__, LogHandler)
