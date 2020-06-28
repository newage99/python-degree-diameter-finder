from misc.globals import get_symbol_classes_that_inherit_from
from symbols.numbers.Number import Number


def get_constants_chars_list():
    numbers = get_symbol_classes_that_inherit_from("Constant", "symbol")
    return ''.join([o for o in numbers])


class Constant(Number):

    __constants = None

    @staticmethod
    def constants():
        if not Constant.__constants:
            Constant.__numbers = get_constants_chars_list()
        return Constant.__constants

    @staticmethod
    def symbol():
        raise NotImplementedError
