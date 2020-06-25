from symbols.interpretable_symbol.functions.Function import Function


class SingleArgFunction(Function):

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol):
        raise NotImplementedError

    @staticmethod
    def forbidden_next_symbol(symbol):
        raise NotImplementedError

    @staticmethod
    def get_number_of_args():
        return 1

    @staticmethod
    def compute(args):
        raise NotImplementedError
