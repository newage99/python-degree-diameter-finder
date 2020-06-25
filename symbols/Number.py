from symbols.Symbol import Symbol, get_symbol_folder_classes


def get_numbers_chars_list():
    numbers = get_symbol_folder_classes("Number", "symbol")
    numbers_list = None
    try:
        numbers_list = [numbers[o][0].symbol() for o in numbers]
    except Exception as e:
        pass
    return ''.join(numbers_list)


class Number(Symbol):

    __numbers = None

    @staticmethod
    def numbers():
        if not Number.__numbers:
            Number.__numbers = get_numbers_chars_list()
        return Number.__numbers

    @staticmethod
    def symbol():
        raise NotImplementedError

    @staticmethod
    def forbidden_prev_symbol(symbol):
        from symbols.Variable import Variable
        return isinstance(symbol, Number) or isinstance(symbol, Variable) or symbol.symbol() == ")"

    @staticmethod
    def forbidden_next_symbol(symbol):
        from symbols.Variable import Variable
        return isinstance(symbol, Number) or isinstance(symbol, Variable) or symbol.symbol() == "("
