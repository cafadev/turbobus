class CommandBusException(Exception):
    pass


class CommandAlreadyExist(CommandBusException):
    pass


class CommandHandlerDoesNotExist(CommandBusException):
    pass


class IncompatibleHandlerReturnType(Exception):

    def __init__(self, class_name, expected_return_type, received_return_type):
        super().__init__(
            f"Incompatible return type - expected {expected_return_type} but got {received_return_type} in {class_name}"
        )

class IncompatibleCommandType(Exception):

    def __init__(self, class_name, expected_command_type, received_command_type):
        super().__init__(
            f"Incompatible command type - expected {expected_command_type} but got {received_command_type} in {class_name}"
        )