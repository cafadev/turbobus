from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid

from turbobus.command import Command, CommandHandler, strict
from turbobus.bus import CommandBus
from turbobus.injection import inject


@dataclass
class UserEntity:
    uuid: uuid.UUID
    name: str


# We're passing the CreateUserHandlerType
# to the Command abstract class. To allow
# the command bus to know the return type of this command
@dataclass
class CreateUserCommand(Command[CreateUserHandlerType]):
    name: str


class IUserRepository(ABC):

    @abstractmethod
    def save(self, user: UserEntity) -> None:
        ...


@inject
class CreateUserCommandHandler(CommandHandler[UserEntity]):
    
    user_repository: IUserRepository

    def execute(self, cmd: CreateUserCommand) -> UserEntity:
        user = UserEntity(uuid.uuid4(), cmd.name)
        self.user_repository.save(user)

        return user


class InMemoryUserRepository(IUserRepository):

    db: dict[str, UserEntity] = {}

    @strict
    def save(self, user: UserEntity) -> None:
        self.db.__setitem__(str(user.uuid), user)

        print(self.db)


if __name__ == '__main__':
    bus = CommandBus()

    user = bus.execute(
        CreateUserCommand('John Due')
    )

