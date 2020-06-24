from symbols.Minus import Minus
from symbols.Operator import Operator


class Subtraction(Minus, Operator):

    @staticmethod
    def has_valid_prev_char(prev_number_or_symbol):
        return prev_number_or_symbol != "" and str(prev_number_or_symbol) != '(' and not isinstance(
            prev_number_or_symbol, Operator)

    def check_symbol(self, char, prev_number_or_symbol):
        return char == self.symbol() and Subtraction.has_valid_prev_char(prev_number_or_symbol)

    def compute(self, args):
        return args[0] - args[1]
