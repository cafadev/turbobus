from turbobus.bus import CommandBus

from log.axioma import LogCommand

bus = CommandBus()

result = bus.execute(
    LogCommand('Hello world')
)