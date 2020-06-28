import random

from misc.globals import get_symbol_classes_that_inherit_from
from symbols.interpretable_symbol.functions.Function import Function


def get_operator_chars():
    operators = get_symbol_classes_that_inherit_from("Operator", "symbol")
    return ''.join([operators[o][0].symbol() for o in operators])


class Operator(Function):

    starting_symbol = False

    __operators = None

    @staticmethod
    def operators():
        if not Operator.__operators:
            Operator.__operators = get_operator_chars()
        return Operator.__operators

    @staticmethod
    def symbol():
        raise NotImplementedError

    def check_symbol(self, char, prev_num_or_symb):
        return char == self.symbol() and prev_num_or_symb != "" and not Operator.forbidden_prev_symbol(prev_num_or_symb)

    @staticmethod
    def forbidden_prev_symbol(symbol):
        from symbols.interpretable_symbol.functions.single_arg_functions.SingleArgFunction import SingleArgFunction
        return isinstance(symbol, Operator) or isinstance(symbol, SingleArgFunction) or str(symbol) == "("

    @staticmethod
    def get_number_of_args():
        return 2

    @staticmethod
    def compute(args):
        raise NotImplementedError

    @staticmethod
    def random():
        return random.choice(Operator.operators())
