import misc.globals as globals

from classes.interpretable_symbols.InterpretableSymbol import InterpretableSymbol
from classes.numbers.Number import Number
from classes.interpretable_symbols.functions.Function import Function
from classes.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction


class CloseParenthesis(InterpretableSymbol):

    starting_symbol = False

    @staticmethod
    def symbol():
        return ")"

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        return symbol is None or isinstance(symbol, Function) or str(symbol) == "("

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Number) or (symbol and str(symbol) == "(") or isinstance(symbol, SingleArgFunction)

    def interpret(self):
        if globals.numbers_count() == 1:
            globals.push_number(globals.numbers.pop()[0])
            globals.functions.pop()
        else:
            raise Exception
