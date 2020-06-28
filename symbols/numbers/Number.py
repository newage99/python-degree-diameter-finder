from misc.globals import get_symbol_classes_that_inherit_from
from symbols.Symbol import Symbol


def get_numbers_chars_list():
    numbers = get_symbol_classes_that_inherit_from("Number", "symbol")
    return ''.join([o for o in numbers])


class Number(Symbol):

    __numbers = None

    @staticmethod
    def numbers():
        if not Number.__numbers:
            Number.__numbers = get_numbers_chars_list()
        return Number.__numbers

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        return isinstance(symbol, Number) or (symbol and str(symbol) == ")")

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Number) or (symbol and str(symbol) == "(")
