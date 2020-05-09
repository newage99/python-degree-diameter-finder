from abc import ABC, abstractmethod


class Command(ABC):

    @staticmethod
    @abstractmethod
    def str_to_execute_command():
        pass

    @staticmethod
    @abstractmethod
    def description():
        pass

    @staticmethod
    @abstractmethod
    def print_help():
        pass

    @staticmethod
    @abstractmethod
    def execute(arguments):
        pass
