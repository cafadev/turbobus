from datetime import date
from turbobus.command import Command, CommandHandler, kw_only_frozen


@kw_only_frozen
class CalculateAgeCommand(Command[int]):

    birthdate: str | date


class CalculateAgeHandler(CommandHandler[CalculateAgeCommand]):

    def execute(self, cmd: CalculateAgeCommand) -> int:
        birthdate: date = cmd.birthdate if isinstance(cmd.birthdate, date) else date.fromisoformat(cmd.birthdate)

        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
