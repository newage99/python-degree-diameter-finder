from abc import abstractmethod
from main.ExpressionInterpreter import ExpressionInterpreter
from symbols.Symbol import Symbol


class Function(Symbol):

    @staticmethod
    @abstractmethod
    def get_number_of_args():
        pass

    def get_arguments(self):
        args = []
        for i in range(self.get_number_of_args()):
            args.insert(0, ExpressionInterpreter.pop_number())
        return args

    @abstractmethod
    def compute(self, args):
        pass

    def is_ready_to_compute(self):
        return ExpressionInterpreter.numbers_count() == self.get_number_of_args()

    def process(self):
        ExpressionInterpreter.functions.append(self)
