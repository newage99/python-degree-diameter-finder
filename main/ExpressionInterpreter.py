import importlib.util
import unittest

from os import listdir
from os.path import isfile, join
from symbols.Symbol import Symbol


class ExpressionInterpreter(unittest.TestCase):

    expression = ''  # Expression to interpret
    pos = 0          # Actual position of the expression we are processing
    numbers = []     # List of tuples indicating the pairs of numbers pending to be merged
    """
    Dict of all non-abstract classes that inherit from Symbol. Each key is the implemented symbol() function returning
    char mapping to a list of all Symbol classes that his symbol() function return that char.
    """
    symbols = {}
    """
    As the interpreter keeps reading the expression, this list gets added functions (single argument functions or
    operators) waiting to be computed. When a function computes his input/s, it gets removed from the list.
    """
    functions = []

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    @staticmethod
    def __get_symbol(char, prev_number_or_symbol):
        if char in ExpressionInterpreter.symbols:
            for symbol in ExpressionInterpreter.symbols[char]:
                if symbol.check_symbol(char, prev_number_or_symbol):
                    return symbol
        raise Exception

    @staticmethod
    def __get_next_number_or_symbol(prev_number_or_symbol):
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
            number_or_symbol = ExpressionInterpreter.__get_symbol(char, prev_number_or_symbol)
        return char, number_or_symbol

    @staticmethod
    def __fill_symbols_dict():
        ExpressionInterpreter.symbols = {}
        excludes = ["Symbol.py", "Function.py", "Operator.py", "SingleArgFunction.py"]
        command_folder_files = [f for f in listdir("../symbols") if isfile(join("../symbols", f)) and f not in excludes]
        for file in command_folder_files:
            spec = importlib.util.spec_from_file_location("", "./../symbols/" + file)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            klass = getattr(foo, file.replace(".py", ""))
            if issubclass(klass, Symbol):
                obj = klass()
                symbol = obj.symbol()
                if symbol in ExpressionInterpreter.symbols:
                    ExpressionInterpreter.symbols[symbol].append(obj)
                else:
                    ExpressionInterpreter.symbols[symbol] = [obj]

    @staticmethod
    def __compute_if_needed():
        last_functions = ExpressionInterpreter.functions[-1]
        while len(last_functions) > 0:
            function = last_functions[-1]
            if function.is_ready_to_compute():
                ExpressionInterpreter.push_number(function.compute(function.get_arguments()))
                last_functions.pop()
            else:
                break

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
        ExpressionInterpreter.functions = []
        ExpressionInterpreter.functions.append([])
        ExpressionInterpreter.__fill_symbols_dict()
        try:
            char, number_or_symbol = ExpressionInterpreter.__get_next_number_or_symbol("")
            while char:
                if type(number_or_symbol) is int:
                    ExpressionInterpreter.push_number(number_or_symbol)
                    ExpressionInterpreter.__compute_if_needed()
                else:
                    number_or_symbol.process()
                    if char == ')':
                        ExpressionInterpreter.__compute_if_needed()
                char, number_or_symbol = ExpressionInterpreter.__get_next_number_or_symbol(number_or_symbol)
        except Exception as e:
            return 0
        return ExpressionInterpreter.numbers[0][0]
