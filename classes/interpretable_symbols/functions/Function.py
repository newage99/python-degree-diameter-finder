import misc.globals as globals

from abc import abstractmethod
from classes.interpretable_symbols.InterpretableSymbol import InterpretableSymbol


class Function(InterpretableSymbol):

    ending_symbol = False
    __symbols_list = None

    @staticmethod
    def symbols():
        if not Function.__symbols_list:
            Function.__symbols_list = []
            symbols_dict = globals.get_symbol_classes_that_inherit_from("Function", "symbol")
            for value in symbols_dict.values():
                Function.__symbols_list += value
        return Function.__symbols_list

    @staticmethod
    @abstractmethod
    def get_number_of_args():
        pass

    @staticmethod
    @abstractmethod
    def compute(args):
        pass

    @staticmethod
    def forbidden_next_symbol(symbol):
        from classes.interpretable_symbols.functions.operators.Operator import Operator
        return isinstance(symbol, Operator) or str(symbol) == ")"

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from classes.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, Function.symbols())

    def interpret(self):
        globals.functions[-1].append(self)

    def get_arguments(self):
        args = []
        for i in range(self.get_number_of_args()):
            args.insert(0, globals.pop_number())
        return args

    def is_ready_to_compute(self):
        return globals.numbers_count() >= self.get_number_of_args()
