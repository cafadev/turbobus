from turbobus.command import CommandBus
from context.calculate_age import CalculateAgeCommand

if __name__ == '__main__':
    bus = CommandBus()

    result = bus.execute(
        CalculateAgeCommand(birthdate='1994-03-09')
    )

    print(f'You are {result} years old')
