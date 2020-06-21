import importlib.util
import unittest

from os import listdir
from os.path import isfile, join


class ExpressionInterpreter(unittest.TestCase):

    expression = ''  # Expression to interpret
    pos = 0          # Actual position of the expression we are processing
    numbers = []     # List of tuples indicating the pairs of numbers pending to be merged
    symbols = []     # List of all non-abstract classes that inherit from Symbol
    """
    As the interpreter keeps reading the expression, this list gets added functions (single argument functions or
    operators) waiting to be computed. When a function computes his input/s, it gets removed from the list.
    """
    functions = []

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    @staticmethod
    def __get_symbol(char, prev_char):
        for symbol in ExpressionInterpreter.symbols:
            if symbol.check_symbol(char, prev_char):
                return symbol
        raise Exception

    @staticmethod
    def __get_next_number_or_symbol(prev_char):
        expression = ExpressionInterpreter.expression
        if ExpressionInterpreter.pos >= len(expression):
            return None, None
        char = expression[ExpressionInterpreter.pos]
        ExpressionInterpreter.pos += 1
        if char.isdigit():
            while ExpressionInterpreter.pos < len(expression) and expression[ExpressionInterpreter.pos].isdigit():
                char += expression[ExpressionInterpreter.pos]
                ExpressionInterpreter.pos += 1
            number_or_symbol = int(char)
        else:
            number_or_symbol = ExpressionInterpreter.__get_symbol(char, prev_char)
        return char, number_or_symbol

    @staticmethod
    def __fill_symbols_list():
        symbol_list = []
        exclude_list = ["Symbol.py", "Function.py", "Operator.py", "SingleArgFunction.py"]
        command_folder_files = [f for f in listdir("../symbols") if isfile(join("../symbols", f)) and f not in exclude_list]
        for file in command_folder_files:
            spec = importlib.util.spec_from_file_location("", "symbols/" + file)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            klass = getattr(foo, file.replace(".py", ""))
            if issubclass(klass, Symbol):
                symbol_list.append(klass)
        return symbol_list

    # --------------------------- #
    # -- PUBLIC STATIC METHODS -- #
    # --------------------------- #

    @staticmethod
    def numbers_count():
        return len(ExpressionInterpreter.numbers[-1])

    @staticmethod
    def pop_number():
        return ExpressionInterpreter.numbers[-1].pop()

    @staticmethod
    def push_number(a):
        ExpressionInterpreter.numbers[-1].append(a)

    @staticmethod
    def compute(expression: str):
        ExpressionInterpreter.expression = expression
        ExpressionInterpreter.numbers = []
        ExpressionInterpreter.numbers.append([])
        ExpressionInterpreter.pos = 0
        ExpressionInterpreter.symbols = ExpressionInterpreter.__fill_symbols_list()
        ExpressionInterpreter.functions = []
        try:
            char, number_or_symbol = ExpressionInterpreter.__get_next_number_or_symbol("")
            while char:
                if type(number_or_symbol) is int:
                    ExpressionInterpreter.push_number(number_or_symbol)
                    if len(ExpressionInterpreter.functions) > 0:
                        function = ExpressionInterpreter.functions[-1]
                        if function.is_ready_to_compute():
                            ExpressionInterpreter.push_number(function.compute(function.get_arguments()))
                            ExpressionInterpreter.functions.pop()
                else:
                    number_or_symbol.process()
                char, number_or_symbol = ExpressionInterpreter.__get_next_number_or_symbol(char)
        except Exception as e:
            return 0
        return ExpressionInterpreter.numbers[0][0]