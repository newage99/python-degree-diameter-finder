from abc import ABC, abstractmethod


class Command(ABC):

    @property
    @abstractmethod
    def str_to_execute_command(self):
        pass

    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def execute(self):
        pass
