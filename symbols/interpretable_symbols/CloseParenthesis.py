import misc.globals as globals

from symbols.interpretable_symbols.InterpretableSymbol import InterpretableSymbol
from symbols.numbers.Number import Number
from symbols.interpretable_symbols.functions.Function import Function
from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction


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
