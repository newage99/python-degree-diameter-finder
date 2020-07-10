from classes.interpretable_symbols.functions.operators.Operator import Operator


class Addition(Operator):

    @staticmethod
    def symbol():
        return "+"

    @staticmethod
    def forbidden_next_symbol(symbol):
        from classes.interpretable_symbols.functions.operators.Operator import Operator
        return isinstance(symbol, Operator) or str(symbol) == ")" or str(symbol) == "-"

    def compute(self, args):
        return args[0] + args[1]
