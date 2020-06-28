import misc.globals as globals
from symbols.interpretable_symbols.InterpretableSymbol import InterpretableSymbol


class ExpressionInterpreter:

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    @staticmethod
    def __get_symbol(char, prev_number_or_symbol) -> InterpretableSymbol:
        if char in InterpretableSymbol.interpretable_symbols_dict():
            for symbol in InterpretableSymbol.interpretable_symbols_dict()[char]:
                if symbol.check_symbol(char, prev_number_or_symbol):
                    return symbol
        raise Exception

    @staticmethod
    def __read_digits(char):
        while globals.pos < len(globals.expression) and globals.expression[globals.pos].isdigit():
            char += globals.expression[globals.pos]
            globals.pos += 1
        return int(char)

    @staticmethod
    def __get_next_number_or_symbol(prev_number_or_symbol):
        read_digits = ExpressionInterpreter.__read_digits
        get_symbol = ExpressionInterpreter.__get_symbol
        if globals.pos >= len(globals.expression):
            return None, None
        char = globals.expression[globals.pos]
        globals.pos += 1
        return char, read_digits(char) if char.isdigit() else get_symbol(char, prev_number_or_symbol)

    @staticmethod
    def __compute_if_needed():
        last_functions = globals.functions[-1]
        while len(last_functions) > 0:
            function = last_functions[-1]
            if function.is_ready_to_compute():
                globals.push_number(function.compute(function.get_arguments()))
                last_functions.pop()
            else:
                break

    # --------------------------- #
    # -- PUBLIC STATIC METHODS -- #
    # --------------------------- #

    @staticmethod
    def compute(expression_to_compute: str):
        globals.expression = expression_to_compute
        globals.numbers = []
        globals.numbers.append([])
        globals.pos = 0
        globals.functions = []
        globals.functions.append([])
        try:
            char, number_or_symbol = ExpressionInterpreter.__get_next_number_or_symbol("")
            while char:
                if type(number_or_symbol) is int:
                    globals.push_number(number_or_symbol)
                    ExpressionInterpreter.__compute_if_needed()
                else:
                    number_or_symbol.interpret()
                    if char == ')':
                        ExpressionInterpreter.__compute_if_needed()
                char, number_or_symbol = ExpressionInterpreter.__get_next_number_or_symbol(number_or_symbol)
        except Exception as e:
            return 0
        return globals.numbers[0][0]
