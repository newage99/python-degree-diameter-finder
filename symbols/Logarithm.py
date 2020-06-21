from math import log
from symbols.Operator import Operator


class Logarithm(Operator):

    def symbol(self):
        return "L"

    def compute(self, args):
        if args[1] == 0:
            raise ValueError
        return log(args[1], args[0])
