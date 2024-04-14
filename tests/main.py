from tests.log.capabilities.log import LogCommand, test_dependency_function_injection_on_logger, test_dependency_injection_on_logger
from turbobus.command import CommandBus


from tests.log.capabilities.log import LogCommand, LogHandler
from turbobus.constants import Provider

from tests.log.axioma.logger import ILogger
from tests.log.capabilities.logger import Logger, Logger2


Provider.set(ILogger.__name__, Logger)
Provider.set('ILogger2', Logger2)
Provider.set(LogCommand.__name__, LogHandler)


if __name__ == '__main__':

    # print('\n\n\nStarting', providers)
    
    bus = CommandBus()

    cmd = LogCommand(content='Done')

    result = bus.execute(
        cmd
    )

# bus = CommandBus()

# cmd = LogCommand(content='Hello world')

# result = bus.execute(
#     cmd
# )

test_dependency_injection_on_logger()
test_dependency_function_injection_on_logger()
