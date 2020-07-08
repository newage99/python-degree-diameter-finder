from math import sqrt

from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction


class SquareRoot(SingleArgFunction):

    @staticmethod
    def symbol():
        return "√"

    def compute(self, args):
        if args[0] < 0:
            raise Exception
        return sqrt(args[0])
