from misc.globals import get_symbol_classes_that_inherit_from
from symbols.numbers.Number import Number


def get_constants_chars_list():
    numbers = get_symbol_classes_that_inherit_from("Constant", "symbol")
    return ''.join([o for o in numbers])


class Constant(Number):

    __constants = None
    __symbols_list = None

    @staticmethod
    def symbols():
        if not Constant.__symbols_list:
            Constant.__symbols_list = []
            symbols_dict = get_symbol_classes_that_inherit_from("Constant", "symbol")
            for value in symbols_dict.values():
                Constant.__symbols_list += value
        return Constant.__symbols_list

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from symbols.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, Constant.symbols())

    @staticmethod
    def constants():
        if not Constant.__constants:
            Constant.__numbers = get_constants_chars_list()
        return Constant.__constants

    @staticmethod
    def symbol():
        raise NotImplementedError
