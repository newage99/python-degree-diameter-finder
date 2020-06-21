from abc import abstractmethod
from symbols.Function import Function
from misc.global_variables import vars_numbers_and_close_parenthesis


class Operator(Function):

    allowed_prev_chars = vars_numbers_and_close_parenthesis

    @staticmethod
    def get_number_of_args():
        return 2

    @abstractmethod
    def compute(self, args):
        pass
