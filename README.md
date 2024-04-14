# TurboBus

TurboBus is a package to create software following the Command Responsibility Segregation pattern in python.

## Installation
```bash
pip install turbobus
```

## Simple usage
Let's see an example using python typings. You can omit all the typing stuffs if you want to.

**God Mode ⚡**
```python3
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

```

**Human Mode (No types, obviously 🙄)**

Here's the same example, but without types
```python3
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

```

## Dependency injection
In many cases we're going to need to inject dependencies to our command handler. To accomplish that we have the `@inject` decorator. For example:

```python3
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

```
@inject(alias={ 'logger': 'ILogger' }, only=['logger'], exclude=['x'])
The `@inject` decorator also accepts the next parameters:

### Alias

The `@inject` decorator use the typing to resolve the required dependency. With the `alias: dict[str, Callable[..., Any]]` parameter you can specify a different implementation for the same interface. For example, let's say we have a UserRepository interface and then two different implementations; UserRepositoryInMemory and UserRepositorySQL.

```python3
Provider.set(UserRepository, UserRepositoryInMemory)
Provider.set('UserRepositorySQL', UserRepositorySQL)

@inject
class CreateUserAccount:

    user: UserRepository
```

By default, the `@inject` will use the `UserRepositoryInMemory` to provide the dependency. Let's specify the `UserRepositorySQL` as the provider. To accomplish that we just need to specify the parameter name that we want to override, and then the Provider Key:


```python3
Provider.set(UserRepository, UserRepositoryInMemory)
Provider.set(UserRepositorySQL, UserRepositorySQL)

@inject(alias = { 'user': 'UserRepositorySQL' })
class CreateUserAccount:

    user: UserRepository
```
