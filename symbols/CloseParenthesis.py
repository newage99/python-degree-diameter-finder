import misc.globals as globals

from symbols.InterpretableSymbol import InterpretableSymbol
from symbols.Number import Number
from symbols.Operator import Operator
from symbols.Variable import Variable


class CloseParenthesis(InterpretableSymbol):

    @staticmethod
    def symbol():
        return ")"

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return isinstance(symbol, Operator) or symbol.symbol() == "("

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Number) or isinstance(symbol, Variable) or symbol.symbol() == "("

    def interpret(self):
        if globals.numbers_count() == 1:
            globals.push_number(globals.numbers.pop()[0])
            globals.functions.pop()
        else:
            raise Exception
