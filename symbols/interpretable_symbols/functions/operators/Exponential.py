from math import pow
from symbols.interpretable_symbols.functions.operators.Operator import Operator


class Exponential(Operator):

    @staticmethod
    def symbol():
        return "^"

    def compute(self, args):
        return pow(args[0], args[1])
