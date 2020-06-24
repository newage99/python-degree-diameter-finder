from symbols.Operator import Operator
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
