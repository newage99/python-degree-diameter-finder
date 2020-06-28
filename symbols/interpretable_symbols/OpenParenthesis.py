import misc.globals as globals

from symbols.numbers.Number import Number
from symbols.interpretable_symbols.functions.operators.Operator import Operator
from symbols.interpretable_symbols.InterpretableSymbol import InterpretableSymbol


class OpenParenthesis(InterpretableSymbol):

    ending_symbol = False

    @staticmethod
    def symbol():
        return "("

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        return isinstance(symbol, Number) or (symbol and str(symbol) == ")")

    @staticmethod
    def forbidden_next_symbol(symbol):
        return symbol is None or isinstance(symbol, Operator) or str(symbol) == ")"

    def interpret(self):
        globals.numbers.append([])
        globals.functions.append([])
