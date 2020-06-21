from symbols.Symbol import Symbol
from main.ExpressionInterpreter import ExpressionInterpreter


class CloseParenthesis(Symbol):

    def symbol(self):
        return ")"

    def process(self):
        if ExpressionInterpreter.numbers_count() == 1:
            ExpressionInterpreter.push_number(ExpressionInterpreter.numbers.pop()[0])
        else:
            raise Exception
