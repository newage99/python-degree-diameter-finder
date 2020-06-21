from symbols.Operator import Operator


class Subtraction(Operator):

    @staticmethod
    def symbol():
        return "-"

    def check_symbol(self, char, prev_char):
        return char == self.symbol() and prev_char in Operator.allowed_prev_chars

    def compute(self, args):
        return args[0] - args[1]
