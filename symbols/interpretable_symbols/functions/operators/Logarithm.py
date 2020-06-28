from math import log
from symbols.interpretable_symbols.functions.operators.Operator import Operator


class Logarithm(Operator):

    @staticmethod
    def symbol():
        return "L"

    def compute(self, args):
        if args[0] == 0 or args[1] == 0:
            raise ValueError
        return log(args[1], args[0])
