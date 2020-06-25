import random

from misc.globals import get_symbol_classes_that_inherit_from
from symbols.interpretable_symbol.functions.Function import Function


def get_operator_chars():
    operators = get_symbol_classes_that_inherit_from("Operator", "symbol")
    return ''.join([operators[o][0].symbol() for o in operators])


class Operator(Function):

    __operators = None

    @staticmethod
    def operators():
        if not Operator.__operators:
            Operator.__operators = get_operator_chars()
        return Operator.__operators

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return isinstance(symbol, Operator) or symbol.symbol() == "-" or symbol.symbol() == "("

    @staticmethod
    def forbidden_next_symbol(symbol):
        return (isinstance(symbol, Operator) and symbol.symbol() != "-") or symbol.symbol() == ")"

    @staticmethod
    def get_number_of_args():
        return 2

    @staticmethod
    def compute(args):
        raise NotImplementedError

    @staticmethod
    def choice():
        return random.choice(Operator.operators())
