from datetime import date
from turbobus.command import Command, CommandBus, CommandHandler, kw_only_frozen
from turbobus.constants import Provider


class CalculateAgeCommand(Command):

    def __init__(self, birthdate):
        self.birthdate = birthdate


class CalculateAgeHandler(CommandHandler):

    def execute(self, cmd: CalculateAgeCommand):
        birthdate = cmd.birthdate if isinstance(cmd.birthdate, date) else date.fromisoformat(cmd.birthdate)

        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

Provider.set(CalculateAgeCommand, CalculateAgeHandler)

if __name__ == '__main__':
    bus = CommandBus()

    result = bus.execute(
        CalculateAgeCommand(birthdate='1994-03-09')
    )

    print(f'You are {result} years old')
