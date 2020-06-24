import misc.globals as globals

from symbols.Number import Number
from symbols.Operator import Operator
from symbols.Variable import Variable
from symbols.InterpretableSymbol import InterpretableSymbol


class OpenParenthesis(InterpretableSymbol):

    @staticmethod
    def symbol():
        return "("

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return isinstance(symbol, Number) or isinstance(symbol, Variable) or symbol.symbol() == ")"

    @staticmethod
    def forbidden_next_symbol(symbol):
        return (isinstance(symbol, Operator) and symbol.symbol() != "-") or symbol.symbol() == ")"

    def interpret(self):
        globals.numbers.append([])
        globals.functions.append([])
