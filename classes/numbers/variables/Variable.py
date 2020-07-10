from misc.globals import get_symbol_classes_that_inherit_from
from classes.numbers.Number import Number


def get_variables_chars_list():
    variables = get_symbol_classes_that_inherit_from("Variable", "symbol")
    return ''.join([variables[o][0].symbol() for o in variables])


class Variable(Number):

    __variables = None
    __symbols_list = None

    @staticmethod
    def symbols():
        if not Variable.__symbols_list:
            Variable.__symbols_list = []
            symbols_dict = get_symbol_classes_that_inherit_from("Variable", "symbol")
            for value in symbols_dict.values():
                Variable.__symbols_list += value
        return Variable.__symbols_list

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from classes.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, Variable.symbols())

    @staticmethod
    def variables():
        if not Variable.__variables:
            Variable.__variables = get_variables_chars_list()
        return Variable.__variables

    @staticmethod
    def symbol():
        raise NotImplementedError
