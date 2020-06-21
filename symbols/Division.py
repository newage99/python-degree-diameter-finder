from symbols.Operator import Operator


class Division(Operator):

    def symbol(self):
        return "/"

    def compute(self, args):
        if args[1] == 0:
            raise ZeroDivisionError
        return args[0] / args[1]
