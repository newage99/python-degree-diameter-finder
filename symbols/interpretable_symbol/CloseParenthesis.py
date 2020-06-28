import misc.globals as globals

from symbols.interpretable_symbol.InterpretableSymbol import InterpretableSymbol
from symbols.numbers.Number import Number
from symbols.interpretable_symbol.functions.operators.Operator import Operator
from symbols.variables.Variable import Variable


class CloseParenthesis(InterpretableSymbol):

    starting_symbol = False

    @staticmethod
    def symbol():
        return ")"

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return symbol is None or isinstance(symbol, Operator) or symbol.symbol() == "-" or symbol.symbol() == "("

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Number) or isinstance(symbol, Variable) or (symbol and symbol.symbol() == "(")

    def interpret(self):
        if globals.numbers_count() == 1:
            globals.push_number(globals.numbers.pop()[0])
            globals.functions.pop()
        else:
            raise Exception
