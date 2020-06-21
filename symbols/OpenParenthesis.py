from symbols.Symbol import Symbol
from expression_interpreter.ExpressionInterpreter import ExpressionInterpreter


class OpenParenthesis(Symbol):

    def symbol(self):
        return "("

    def process(self):
        ExpressionInterpreter.numbers.append([])
