from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction


class Negation(SingleArgFunction):

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        return str(symbol) == ')' or str(symbol) == '-'

    @staticmethod
    def symbol():
        return "-"

    def compute(self, args):
        return -args[0]
