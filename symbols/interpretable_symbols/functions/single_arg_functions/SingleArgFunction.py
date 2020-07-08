from misc.globals import get_symbol_classes_that_inherit_from
from symbols.interpretable_symbols.functions.Function import Function


class SingleArgFunction(Function):

    __symbols_list = None

    @staticmethod
    def symbols():
        if not SingleArgFunction.__symbols_list:
            SingleArgFunction.__symbols_list = []
            symbols_dict = get_symbol_classes_that_inherit_from("SingleArgFunction", "symbol")
            for value in symbols_dict.values():
                SingleArgFunction.__symbols_list += value
        return SingleArgFunction.__symbols_list

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        from symbols.numbers.Number import Number
        return str(symbol) == ")" or isinstance(symbol, Number)

    @staticmethod
    def forbidden_next_symbol(symbol):
        from symbols.interpretable_symbols.functions.operators.Operator import Operator
        return isinstance(symbol, Operator) or str(symbol) == ")"

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from symbols.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, SingleArgFunction.symbols())

    @staticmethod
    def get_number_of_args():
        return 1

    @staticmethod
    def compute(args):
        raise NotImplementedError
