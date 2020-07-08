from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction


class Negation(SingleArgFunction):

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        from symbols.interpretable_symbols.functions.operators.Operator import Operator
        return str(symbol) == ")" or (isinstance(symbol, Operator) and str(symbol) == "+") or str(symbol) == "-"

    @staticmethod
    def forbidden_next_symbol(symbol):
        from symbols.interpretable_symbols.functions.operators.Operator import Operator
        return isinstance(symbol, Operator) or str(symbol) == ")" or str(symbol) == "-"

    @staticmethod
    def symbol():
        return "-"

    def compute(self, args):
        return -args[0]
