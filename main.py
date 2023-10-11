from log.axioma import LogCommand
# from log.capabilities.log import Logger
from turbobus import bus


bus = bus.CommandBus()

result = bus.execute(
    LogCommand('Hello Christopher')
)

print(result)