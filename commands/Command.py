from abc import ABC, abstractmethod


class Command(ABC):

    @staticmethod
    @abstractmethod
    def str_to_execute_command():
        pass

    @staticmethod
    @abstractmethod
    def help():
        pass

    @staticmethod
    @abstractmethod
    def execute():
        pass
