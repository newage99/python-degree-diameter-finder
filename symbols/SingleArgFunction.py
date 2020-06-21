from symbols.Function import Function
from abc import abstractmethod


class SingleArgFunction(Function):

    @staticmethod
    def get_number_of_args():
        return 1

    @abstractmethod
    def compute(self, args):
        pass
