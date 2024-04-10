from abc import ABC, abstractmethod


class ILogger(ABC):

    @abstractmethod
    def print(self, text: str):
        ...
