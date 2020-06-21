from symbols.Function import Function
from expression_interpreter.ExpressionInterpreter import ExpressionInterpreter
from abc import abstractmethod


class SingleArgFunction(Function):

    @staticmethod
    def get_number_of_args():
        return 1

    @staticmethod
    def get_arguments():
        return [ExpressionInterpreter.pop_number()]

    @abstractmethod
    def compute(self, args):
        pass
