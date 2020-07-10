from classes.interpretable_symbols.functions.operators.Operator import Operator


class Subtraction(Operator):

    @staticmethod
    def symbol():
        return "-"

    @staticmethod
    def forbidden_next_symbol(symbol):
        return isinstance(symbol, Operator) or str(symbol) == ")" or str(symbol) == "-"

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        from classes.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction
        return isinstance(symbol, Operator) or isinstance(symbol, SingleArgFunction) or str(symbol) == "("

    def compute(self, args):
        return args[0] - args[1]
