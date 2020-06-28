import misc.globals as globals

from symbols.numbers.Number import Number
from symbols.interpretable_symbol.functions.operators.Operator import Operator
from symbols.variables.Variable import Variable
from symbols.interpretable_symbol.InterpretableSymbol import InterpretableSymbol


class OpenParenthesis(InterpretableSymbol):

    @staticmethod
    def symbol():
        return "("

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return isinstance(symbol, Number) or isinstance(symbol, Variable) or (symbol and symbol.symbol() == ")")

    @staticmethod
    def forbidden_next_symbol(symbol):
        return symbol is None or isinstance(symbol, Operator) or symbol.symbol() == ")"

    def interpret(self):
        globals.numbers.append([])
        globals.functions.append([])
