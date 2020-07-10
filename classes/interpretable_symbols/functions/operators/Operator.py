import random

from misc.globals import get_symbol_classes_that_inherit_from
from classes.interpretable_symbols.functions.Function import Function


def get_operator_chars():
    operators = get_symbol_classes_that_inherit_from("Operator", "symbol")
    return ''.join([operators[o][0].symbol() for o in operators])


class Operator(Function):

    starting_symbol = False

    __operators = None
    __symbols_list = None

    @staticmethod
    def symbols():
        if not Operator.__symbols_list:
            Operator.__symbols_list = []
            symbols_dict = get_symbol_classes_that_inherit_from("Operator", "symbol")
            for value in symbols_dict.values():
                Operator.__symbols_list += value
        return Operator.__symbols_list

    @staticmethod
    def operators():
        if not Operator.__operators:
            Operator.__operators = get_operator_chars()
        return Operator.__operators

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        from classes.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction
        return isinstance(symbol, Operator) or isinstance(symbol, SingleArgFunction) or str(symbol) == "("

    @staticmethod
    def get_number_of_args():
        return 2

    @staticmethod
    def compute(args):
        raise NotImplementedError

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from classes.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, Operator.symbols())

    @staticmethod
    def random_operator():
        return random.choice(Operator.operators())
