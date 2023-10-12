# TurboBus

TurboBus is an opinionated implementation of Command Responsibility Segregation pattern in python.

## Simple usage
Let's see an example using python typings. You can omit all the typing stuffs if you want to.

**God Mode ⚡**
```python3
from  dataclasses  import  dataclass
from  typing  import  TypeAlias

from  turbobus.command  import  Command, CommandHandler, CommandBus, handler_of
from  turbobus.injection  import  injectable

LogHandlerType: TypeAlias  =  "ILogHandler"

@dataclass
class  LogCommand(Command[LogHandlerType]):
	content: str  


class  ILogHandler(CommandHandler[LogCommand, str]):
	...


@handler_of(LogCommand)
class  LogHandler(ILogHandler):
	def  execute(self, cmd: LogCommand) -> str:
		return  cmd.content


if __name__ == '__main__':
	bus  =  CommandBus()

	result  =  bus.execute(
		LogCommand('Hello dude!')
	)
	print(result)  # Hello dude
```

**Human Mode 🥱**
```python3
from  dataclasses  import  dataclass

from  turbobus.command  import  Command, CommandHandler, handler_of
from  turbobus.decorators  import injectable

@dataclass
class  LogCommand(Command):
	content


class  ILogHandler(CommandHandler):
	...

@handler_of(LogCommand)
class  LogHandler(ILogHandler):
	def  execute(self, cmd: LogCommand) -> str:
		return  cmd.content


if __name__ == '__main__':
	bus  =  CommandBus()

	result  =  bus.execute(
		LogCommand('Hello dude!')
	)
	print(result)  # Hello dude
```

## Dependency injection
In many cases we're going to need to inject dependencies to our command handler. To accomplish that we have two important tools: `@injectable_of` decorator and `inject` function. 

With the `@injectable_of` decorator we can specify a class that is implementing the functionalities of the dependency. For example:

```python3
from turbobus.injection import injectable_of, inject
from log.axioma.log import ILogger


class ILogger(ABC):

    @abstractmethod
    def logger(self, text: str) -> None:
        ...


@injectable_of(ILogger)
class Logger:

    def logger(self, text: str) -> None:
        print(text)


@command(LogCommand)
@dataclass(kw_only=True)
class LogHandler(ILogHandler):

    logger = inject(ILogger)

    def execute(self, cmd: LogCommand) -> str:
		self.logger.logger(cmd.content)
        return cmd.content

```

As you can see in the example above, we're defining an abstract class with the logger method. Then we're doing the implementation of the `ILogger` and we're indicating that in the `@injectable_of(ILogger)`. 

Then, using the `inject` function, TurboBus is going to map that dependency and inject the instance in the attribute.
