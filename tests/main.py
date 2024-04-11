from tests.log.capabilities.log import LogCommand, test_dependency_function_injection_on_logger
from turbobus.command import CommandBus

from tests.log.capabilities.log import test_dependency_injection_on_logger
from tests.log.capabilities.log import LogCommand

if __name__ == '__main__':

    # print('\n\n\nStarting', providers)
    
    bus = CommandBus()

    cmd = LogCommand(content=1)

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
