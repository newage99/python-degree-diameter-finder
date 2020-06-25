from misc.globals import get_symbol_classes_that_inherit_from
from symbols.numbers.Number import Number
from symbols.Symbol import Symbol


def get_variables_chars_list():
    variables = get_symbol_classes_that_inherit_from("Variable", "symbol")
    return ''.join([variables[o][0].symbol() for o in variables])


class Variable(Symbol):

    __variables = None

    @staticmethod
    def variables():
        if not Variable.__variables:
            Variable.__variables = get_variables_chars_list()
        return Variable.__variables

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return isinstance(symbol, Variable) or isinstance(symbol, Number) or symbol.symbol() == ")"

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Variable) or isinstance(symbol, Number) or symbol.symbol() == "("
