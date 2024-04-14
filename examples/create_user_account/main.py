from abc import ABC, abstractmethod
from dataclasses import field
import uuid
from turbobus.command import Command, CommandBus, CommandHandler, kw_only_frozen
from turbobus.constants import Provider
from turbobus.injection import inject


# This is a simple Entity to represent a User
@kw_only_frozen
class UserEntity:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str
    email: str


# We need to define the repository interface
# to save and retrieve users
class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> UserEntity | None:
        """Get user by id"""

    @abstractmethod
    def save(self, user: UserEntity) -> None:
        """Save user"""


# This is an in-memory implementation of the UserRepository
class UserRepositoryInMemory(UserRepository):

    def __init__(self):
        self._users: dict[uuid.UUID, UserEntity] = {}

    def get_by_id(self, id: uuid.UUID) -> UserEntity | None:
        return self._users.get(id)
    
    def save(self, user: UserEntity) -> None:
        self._users[user.id] = user


# Let's create a command to create a user account
@kw_only_frozen
class CreateUserAccount(Command[None]):
    name: str
    email: str


#  @inject is used to inject the dependencies
@inject
@kw_only_frozen
class CreateUserAccountHandler(CommandHandler[CreateUserAccount]):

    user_repository: UserRepository

    def execute(self, cmd: CreateUserAccount) -> None:
        user = UserEntity(name=cmd.name, email=cmd.email)

        # It's unnecessary to retrieve the user from the repository
        # this is just to demonstrate that the user was saved
        self.user_repository.save(user)
        user = self.user_repository.get_by_id(user.id)

        if user is None:
            raise Exception('User not found')
        
        print(f'Welcome {user.name}!')


Provider.set(UserRepository, UserRepositoryInMemory)
Provider.set(CreateUserAccount, CreateUserAccountHandler)


if __name__ == '__main__':
    bus = CommandBus()

    bus.execute(
        CreateUserAccount(name='Christopher Flores', email='cafadev@outlook.com')
    )