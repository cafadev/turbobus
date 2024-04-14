from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uuid

from turbobus.command import CommandBus, Command, CommandHandler
from turbobus.injection import inject


@dataclass(kw_only=True)
class UserEntity:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str


# We're passing the UserEntity
# to the Command abstract class. To allow
# the command bus to know the return type of this command
@dataclass
class CreateUserCommand(Command[UserEntity]):
    name: str


class IUserRepository(ABC):

    @abstractmethod
    def save(self, user: UserEntity) -> None:
        ...


@inject
class CreateUserCommandHandler(CommandHandler[UserEntity]):
    
    user_repository: IUserRepository

    def execute(self, cmd: CreateUserCommand) -> UserEntity:
        user = UserEntity(
            name=cmd.name
        )

        self.user_repository.save(user)
        return user


class InMemoryUserRepository(IUserRepository):

    db: dict[str, UserEntity] = {}

    def save(self, user: UserEntity) -> None:
        self.db.__setitem__(str(user.id), user)

        print(self.db)


if __name__ == '__main__':
    bus = CommandBus()

    user = bus.execute(
        CreateUserCommand('John Due')
    )

