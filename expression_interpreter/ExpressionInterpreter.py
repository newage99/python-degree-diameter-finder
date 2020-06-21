from expression_interpreter.Symbol import Symbol
from expression_interpreter.Result import Result
from math import log, pow
import unittest
from misc.global_variables import operators


class ExpressionInterpreter(unittest.TestCase):

    expression = ''
    actualSymbol = Symbol.Default
    pos = 0
    numbers = []
    operations = []
    result = Result.OK
    symbols = []

    # char_to_symbol = {
    #     '+': Symbol.Addition,
    #     '-': Symbol.Subtraction,
    #     '*': Symbol.Multiplication,
    #     '/': Symbol.Division,
    #     '%': Symbol.Modulus,
    #     '^': Symbol.Exponential,
    #     'L': Symbol.Logarithm,
    #     '(': Symbol.OpenParenthesis,
    #     ')': Symbol.CloseParenthesis
    # }

    functions = []  # List of

    @staticmethod
    def numbers_count():
        return len(ExpressionInterpreter.numbers[-1])

    @staticmethod
    def pop_number():
        return ExpressionInterpreter.numbers[-1].pop()

    @staticmethod
    def push_number(a):
        ExpressionInterpreter.numbers[-1].append(a)

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    @staticmethod
    def __subtraction(a, b):
        a, b = ExpressionInterpreter.__limits(a, b, bottom_result=0)
        return b - a

    @staticmethod
    def __multiplication(a, b):
        a, b = ExpressionInterpreter.__limits(a, b, bottom_result=0)
        return b * a

    @staticmethod
    def __division(a, b):
        incorrect_input = a == 0
        a, limit_reached = ExpressionInterpreter.__limit(a)
        b, limit_reached = ExpressionInterpreter.__limit(b, bottom_result=0)
        return b / a, incorrect_input

    @staticmethod
    def __modulus(a, b):
        a, b = ExpressionInterpreter.__limits(a, b)
        return b % a

    @staticmethod
    def __exponential(a, b):
        a, limit_reached = ExpressionInterpreter.__limit(a, 100, 0.01)
        if limit_reached:
            return a
        b, limit_reached = ExpressionInterpreter.__limit(b)
        return pow(b, a)

    @staticmethod
    def __logarithm(a, b):
        incorrect_input = a == 0
        a, limit_reached = ExpressionInterpreter.__limit(a, 100, 2, 100, 2)
        b, limit_reached = ExpressionInterpreter.__limit(b)
        return log(a, b), incorrect_input

    @staticmethod
    def __operation_count():
        return len(ExpressionInterpreter.operations[-1])

    @staticmethod
    def __apply_operation():
        if len(ExpressionInterpreter.operations) <= 0:
            return
        count = ExpressionInterpreter.__count()
        if count > 1:
            operation = ExpressionInterpreter.operations.pop()

            if operation == Symbol.Addition:
                ExpressionInterpreter.__push(ExpressionInterpreter.__addition(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop()))
            elif operation == Symbol.Subtraction:
                ExpressionInterpreter.__push(ExpressionInterpreter.__subtraction(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop()))
            elif operation == Symbol.Multiplication:
                ExpressionInterpreter.__push(ExpressionInterpreter.__multiplication(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop()))
            elif operation == Symbol.Division:
                res, incorrect_input = ExpressionInterpreter.__division(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop())
                ExpressionInterpreter.__push(res)
                if incorrect_input:
                    ExpressionInterpreter.result = Result.DivisionByZero
            elif operation == Symbol.Modulus:
                ExpressionInterpreter.__push(ExpressionInterpreter.__modulus(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop()))
            elif operation == Symbol.Exponential:
                ExpressionInterpreter.__push(ExpressionInterpreter.__exponential(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop()))
            elif operation == Symbol.Logarithm:
                res, incorrect_input = ExpressionInterpreter.__logarithm(ExpressionInterpreter.__pop(), ExpressionInterpreter.__pop())
                ExpressionInterpreter.__push(res)
                if incorrect_input:
                    ExpressionInterpreter.result = Result.LogarithmWrongInputs
            else:
                ExpressionInterpreter.result = Result.WrongOperation
        else:
            ExpressionInterpreter.result = Result.NumberStackWrongElements

    @staticmethod
    def __get_next_symbol():
        if ExpressionInterpreter.pos >= len(ExpressionInterpreter.expression):
            return Symbol.ExpressionEnd
        c = ExpressionInterpreter.expression[ExpressionInterpreter.pos]
        ExpressionInterpreter.pos += 1
        expression_not_ended = True
        while type(c) is str and c.isdigit() and expression_not_ended:
            if ExpressionInterpreter.pos >= len(ExpressionInterpreter.expression):
                expression_not_ended = False
                c = int(c)
            else:
                c += ExpressionInterpreter.expression[ExpressionInterpreter.pos]
                ExpressionInterpreter.pos += 1
        if type(c) is str and c[:-1].isdigit():
            c = int(c[:-1])
            ExpressionInterpreter.pos -= 1
        return c

    @staticmethod
    def limit(a, top_threshold=100000000000000, bottom_threshold=0.00000000001, top_result=100000000000000,
                bottom_result=0.00000000001):
        limit_reached = False
        if a > top_threshold:
            a = top_result
            limit_reached = True
        elif a < -top_threshold:
            a = -top_result
            limit_reached = True
        elif (bottom_threshold > a > 0) or a == 0:
            a = bottom_result
            limit_reached = True
        elif -bottom_threshold < a <= 0:
            a = -bottom_result
            limit_reached = True
        return a, limit_reached

    @staticmethod
    def limits(a, b, bottom_result=0.00000000001):
        return ExpressionInterpreter.limit(a, bottom_result=bottom_result)[0], ExpressionInterpreter.limit(b, bottom_result=bottom_result)[0]

    # --------------------------- #
    # -- PUBLIC STATIC METHODS -- #
    # --------------------------- #

    @staticmethod
    def process_negations(expression):
        expression_modified = True
        while expression_modified:
            expression_modified = False
            for i in range(len(expression)):
                if expression[i] == '-' and (i == 0 or expression[i - 1] in (operators + "(").replace("+", "")):
                    final_suffix = expression[i + 1:]
                    if i > 0:
                        parenthesis_counter = 0
                        close_parenthesis_not_added = True
                        for j in range(len(final_suffix)):
                            if final_suffix[j] == '(':
                                parenthesis_counter += 1
                            elif (parenthesis_counter == 0 or (parenthesis_counter == 1 and final_suffix[j] == ')')) \
                                    and (j + 1 == len(final_suffix) or not final_suffix[j:j + 2].isdigit()):
                                final_suffix = final_suffix[:j + 1] + ")" + final_suffix[j + 1:]
                                close_parenthesis_not_added = False
                                break
                            elif final_suffix[j] == ')':
                                parenthesis_counter -= 1
                        if close_parenthesis_not_added:
                            final_suffix += ")"
                    expression = expression[:i] + ("(" if i > 0 else "") + "0-" + final_suffix
                    expression_modified = True
                    break
        return expression

    @staticmethod
    def fill_symbols_list():
        pass  # TODO

    @staticmethod
    def compute(expression: str):

        ExpressionInterpreter.expression = ExpressionInterpreter.process_negations(expression)
        ExpressionInterpreter.numbers = []
        ExpressionInterpreter.numbers.append([])
        ExpressionInterpreter.operations = []
        ExpressionInterpreter.pos = 0
        try:
            c = ExpressionInterpreter.__get_next_symbol()
            while c is not Symbol.ExpressionEnd:
                if c in ExpressionInterpreter.char_to_symbol:
                    c = ExpressionInterpreter.char_to_symbol[c]
                if c == Symbol.OpenParenthesis:
                    ExpressionInterpreter.numbers.append([])
                elif c == Symbol.CloseParenthesis:
                    if ExpressionInterpreter.__count() == 1:
                        ExpressionInterpreter.__push(ExpressionInterpreter.numbers.pop()[0])
                    else:
                        raise Exception
                elif c in ExpressionInterpreter.char_to_symbol.values():
                    ExpressionInterpreter.operations.append(c)
                else:
                    ExpressionInterpreter.__push(c)
                if ExpressionInterpreter.__count() == 2:
                    ExpressionInterpreter.__apply_operation()
                c = ExpressionInterpreter.__get_next_symbol()
        except Exception as e:
            return 0
        if len(ExpressionInterpreter.numbers) <= 0 or len(ExpressionInterpreter.numbers[0]) <= 0:
            a = 0
        return ExpressionInterpreter.numbers[0][0]
