from classes.interpretable_symbols.functions.operators.Operator import Operator


class Modulus(Operator):

    @staticmethod
    def symbol():
        return "%"

    def compute(self, args):
        return args[0] % args[1]
