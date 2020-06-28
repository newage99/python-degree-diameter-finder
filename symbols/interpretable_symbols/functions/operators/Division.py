from symbols.interpretable_symbols.functions.operators.Operator import Operator


class Division(Operator):

    @staticmethod
    def symbol():
        return "/"

    def compute(self, args):
        if args[1] == 0:
            raise ZeroDivisionError
        return args[0] / args[1]
