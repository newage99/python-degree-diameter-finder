from symbols.Minus import Minus
from symbols.SingleArgFunction import SingleArgFunction
from symbols.Subtraction import Subtraction


class Negation(Minus, SingleArgFunction):

    def check_symbol(self, char, prev_number_or_symbol):
        return char == self.symbol() and not Subtraction.has_valid_prev_char(prev_number_or_symbol)

    def compute(self, args):
        return -args[0]
