from symbols.interpretable_symbols.functions.Function import Function


class SingleArgFunction(Function):

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol) -> bool:
        return str(symbol) == ')'

    @staticmethod
    def get_number_of_args():
        return 1

    @staticmethod
    def compute(args):
        raise NotImplementedError
