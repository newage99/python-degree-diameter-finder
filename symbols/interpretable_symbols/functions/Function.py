from symbols.interpretable_symbols.InterpretableSymbol import InterpretableSymbol
import misc.globals as globals

from abc import abstractmethod


class Function(InterpretableSymbol):

    ending_symbol = False

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
        from symbols.interpretable_symbols.functions.operators.Operator import Operator
        return isinstance(symbol, Operator) or str(symbol) == ")"

    def interpret(self):
        globals.functions[-1].append(self)

    def get_arguments(self):
        args = []
        for i in range(self.get_number_of_args()):
            args.insert(0, globals.pop_number())
        return args

    def is_ready_to_compute(self):
        return globals.numbers_count() >= self.get_number_of_args()