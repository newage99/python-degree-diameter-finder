from abc import abstractmethod
from expression_interpreter.ExpressionInterpreter import ExpressionInterpreter
from symbols.Symbol import Symbol


class Function(Symbol):

    @staticmethod
    @abstractmethod
    def get_number_of_args():
        pass

    @staticmethod
    @abstractmethod
    def get_arguments():
        pass

    @abstractmethod
    def compute(self, args):
        pass

    def is_ready_to_compute(self):
        return ExpressionInterpreter.numbers_count() == self.get_number_of_args()

    def process(self):
        ExpressionInterpreter.functions.append(self)
