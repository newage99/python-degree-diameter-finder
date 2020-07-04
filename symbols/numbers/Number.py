from misc.globals import get_symbol_classes_that_inherit_from
from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction
from symbols.Symbol import Symbol


def get_numbers_chars_list():
    numbers = get_symbol_classes_that_inherit_from("Number", "symbol")
    return ''.join([o for o in numbers])


class Number(Symbol):

    __symbols_list = None
    __numbers = None

    @staticmethod
    def symbols():
        if not Number.__symbols_list:
            Number.__symbols_list = []
            symbols_dict = get_symbol_classes_that_inherit_from("Number", "symbol")
            for value in symbols_dict.values():
                Number.__symbols_list += value
        return Number.__symbols_list

    @staticmethod
    def numbers():
        if not Number.__numbers:
            Number.__numbers = get_numbers_chars_list()
        return Number.__numbers

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from symbols.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, Number.symbols())

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        return isinstance(symbol, Number) or (symbol and str(symbol) == ")")

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Number) or (symbol and str(symbol) == "(") or isinstance(symbol, SingleArgFunction)
