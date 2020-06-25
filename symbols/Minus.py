from symbols.interpretable_symbol.functions.operators.Operator import Operator
from symbols.Symbol import Symbol


class Minus(Symbol):

    @staticmethod
    def symbol():
        return "-"

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return symbol.symbol() in ["+", "-"]

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Operator) or symbol.symbol() == ")"

    def check_symbol(self, char, prev_number_or_symbol):
        raise NotImplementedError
