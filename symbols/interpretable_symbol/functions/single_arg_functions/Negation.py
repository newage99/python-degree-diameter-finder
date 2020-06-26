from symbols.interpretable_symbol.functions.single_arg_functions.SingleArgFunction import SingleArgFunction


class Negation(SingleArgFunction):

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return str(symbol) == ')' or str(symbol) == '-'

    def check_symbol(self, char, prev_num_or_symbol):
        return char == self.symbol() and not Negation.forbidden_prev_symbol(prev_num_or_symbol)

    @staticmethod
    def symbol():
        return "-"

    def compute(self, args):
        return -args[0]
