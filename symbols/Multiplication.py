from symbols.Operator import Operator


class Addition(Operator):

    def symbol(self):
        return "*"

    def compute(self, args):
        return args[0] * args[1]
