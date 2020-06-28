from misc.globals import get_symbol_classes_that_inherit_from
from symbols.numbers.Number import Number


def get_variables_chars_list():
    variables = get_symbol_classes_that_inherit_from("Variable", "symbol")
    return ''.join([variables[o][0].symbol() for o in variables])


class Variable(Number):

    __variables = None

    @staticmethod
    def variables():
        if not Variable.__variables:
            Variable.__variables = get_variables_chars_list()
        return Variable.__variables

    @staticmethod
    def symbol():
        raise NotImplementedError
