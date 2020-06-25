from symbols.interpretable_symbol.functions.operators.Operator import Operator


class Multiplication(Operator):

    @staticmethod
    def symbol():
        return "*"

    def compute(self, args):
        return args[0] * args[1]
