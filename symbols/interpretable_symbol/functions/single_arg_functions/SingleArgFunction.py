from symbols.interpretable_symbol.functions.Function import Function


class SingleArgFunction(Function):

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol):
        return str(symbol) == ')'

    def check_symbol(self, char, prev_num_or_symbol):
        return char == self.symbol() and not SingleArgFunction.forbidden_prev_symbol(prev_num_or_symbol)

    @staticmethod
    def get_number_of_args():
        return 1

    @staticmethod
    def compute(args):
        raise NotImplementedError
