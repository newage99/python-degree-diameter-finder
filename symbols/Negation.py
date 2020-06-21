from symbols.SingleArgFunction import SingleArgFunction
from symbols.Operator import Operator


class Negate(SingleArgFunction):

    def symbol(self):
        return "-"

    def check_symbol(self, char, prev_char):
        return char == self.symbol() and prev_char not in Operator.allowed_prev_chars

    def compute(self, args):
        return -args[0]
