from dataclasses import dataclass
from typing import NewType, TypeAlias
import pytest
from turbobus import Command, CommandHandler, CommandBus, kw_only_frozen
from turbobus.constants import Provider
from turbobus.exception import CommandHandlerDoesNotExist, IncompatibleCommandType, IncompatibleHandlerReturnType


SerieValues: TypeAlias = tuple[int, str, bool, int]

def test_command_bus_to_execute_a_command():
    class SampleCommand(Command[int]):
        pass

    class SampleCommandHandler(CommandHandler[SampleCommand]):

        def execute(self, cmd: SampleCommand) -> int:
            return 42

    Provider.clear()
    Provider.set(SampleCommand, SampleCommandHandler)

    bus = CommandBus()

    command = SampleCommand()
    result = bus.execute(command)

    assert type(result) == SampleCommand.__return_type__ # type: ignore
    assert result == 42


def test_command_bus_to_execute_a_command_with_args():

    @kw_only_frozen
    class SampleCommand(Command[SerieValues]):
        value_int: int
        value_str: str
        value_bool: bool
        default_value: int = 42
        

    class SampleCommandHandler(CommandHandler[SampleCommand]):

        def execute(self, cmd: SampleCommand) -> SerieValues:
            return (cmd.value_int, cmd.value_str, cmd.value_bool, cmd.default_value)

    Provider.clear()
    Provider.set(SampleCommand, SampleCommandHandler)

    bus = CommandBus()

    command = SampleCommand(value_int=42, value_str="42", value_bool=True)
    result: SerieValues = bus.execute(command)

    assert type(result) == tuple # type: ignore


def test_register_multiple_commands_and_handlers():

    @kw_only_frozen
    class SampleCommand(Command[int]):
        value: int

    class SampleCommandHandler(CommandHandler[SampleCommand]):

        def execute(self, cmd: SampleCommand) -> int:
            return cmd.value

    @kw_only_frozen
    class AnotherSampleCommand(Command[str]):
        value: str

    class AnotherSampleCommandHandler(CommandHandler[AnotherSampleCommand]):

        def execute(self, cmd: AnotherSampleCommand) -> str:
            return cmd.value

    Provider.clear()
    Provider.set(SampleCommand, SampleCommandHandler)
    Provider.set(AnotherSampleCommand, AnotherSampleCommandHandler)

    bus = CommandBus()

    command_value = 42
    command = SampleCommand(value=command_value)
    result = bus.execute(command)

    assert type(result) == SampleCommand.__return_type__ # type: ignore
    assert result == command_value

    another_command_value = 'Hello'
    command = AnotherSampleCommand(value=another_command_value)
    result = bus.execute(command)

    assert type(result) == AnotherSampleCommand.__return_type__ # type: ignore
    assert result == another_command_value


def test_command_handler_return_type():
    with pytest.raises(IncompatibleHandlerReturnType):
        class InvalidReturnTypeCommand(Command[int]):
            pass

        class InvalidReturnTypeCommandHandler(CommandHandler[InvalidReturnTypeCommand]):

            def execute(self, cmd: InvalidReturnTypeCommand) -> str:
                return "invalid"
            

def test_command_handler_command_type():
    with pytest.raises(IncompatibleCommandType):
        class ValidCommand(Command[int]):
            pass

        class InvalidCommandTypeCommand(Command[int]):
            pass

        class InvalidCommandTypeCommandHandler(CommandHandler[ValidCommand]):

            def execute(self, cmd: InvalidCommandTypeCommand) -> int:
                return 42


def test_command_handler_does_not_exist():

    class ImaginaryCommand(Command[int]):
        pass

    class ImaginaryCommandHandler(CommandHandler[ImaginaryCommand]):
        def execute(self, cmd: ImaginaryCommand) -> int:
            return 42
        
    ########################################
    # Intentionally forget to set the provider
    ########################################

    bus = CommandBus()
    with pytest.raises(CommandHandlerDoesNotExist):
        command = ImaginaryCommand()
        bus.execute(command)
