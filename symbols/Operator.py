from abc import abstractmethod
from symbols.Function import Function


class Operator(Function):

    @staticmethod
    def get_number_of_args():
        return 2

    @abstractmethod
    def compute(self, args):
        pass
