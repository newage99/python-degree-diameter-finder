from symbols.Symbol import Symbol
from main.ExpressionInterpreter import ExpressionInterpreter


class OpenParenthesis(Symbol):

    def symbol(self):
        return "("

    def process(self):
        ExpressionInterpreter.numbers.append([])
