from datetime import date
from turbobus.command import Command, CommandBus, CommandHandler, kw_only_frozen
from turbobus.constants import Provider

# We need to create a Command class that receives the values that the handler will use
# to execute the command. The Command class is a generic class that receives the return

# @kw_only_frozen: is a shortcut decorator for @dataclass(kw_only=True, frozen=True)

# Command[int]: is a generic class that receives a return_type.
# This is useful to check if the handler is returning the correct type
# And allow the CommandBus to know the return type of the command

@kw_only_frozen 
class CalculateAgeCommand(Command[int]):
    birthdate: str | date


# We need to create a CommandHandler class that will receive the Command class.
# The handler class must implement the execute method
    
# CommandHandler[CalculateAgeCommand]: is a generic class that receives the Command class
# this is useful to check if the handler is implementing the correct command class
class CalculateAgeHandler(CommandHandler[CalculateAgeCommand]):

    # The execute method must receive the Command class and return
    # the same type as in the Command class return_type
    def execute(self, cmd: CalculateAgeCommand) -> int:
        birthdate: date = cmd.birthdate if isinstance(cmd.birthdate, date) else date.fromisoformat(cmd.birthdate)

        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age


# We need to register the Command and Handler in the Provider
# This is necessary to allow the CommandBus to find the correct handler
# to execute the command
Provider.set(CalculateAgeCommand, CalculateAgeHandler)


if __name__ == '__main__':
    # We need to create a CommandBus instance to execute the command
    bus = CommandBus()

    # Here we are executing the CalculateAgeCommand
    # if you're using an IDE that supports type hinting
    # you'll see that the result variable is inferred as int
    # because the CalculateAgeCommand is a generic class
    # that receives int as return_type
    result = bus.execute(
        CalculateAgeCommand(birthdate='1994-03-09')
    )

    print(f'You are {result} years old')
