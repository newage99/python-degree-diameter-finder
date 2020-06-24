from symbols.Number import Number
from symbols.Symbol import Symbol, get_symbol_folder_classes


def get_variables_chars_list():
    variables = get_symbol_folder_classes("Variable", "symbol")
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
