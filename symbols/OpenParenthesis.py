from symbols.Symbol import Symbol
from main.ExpressionInterpreter import ExpressionInterpreter


class OpenParenthesis(Symbol):

    @staticmethod
    def symbol():
        return "("

    def process(self):
        ExpressionInterpreter.numbers.append([])
        ExpressionInterpreter.functions.append([])
