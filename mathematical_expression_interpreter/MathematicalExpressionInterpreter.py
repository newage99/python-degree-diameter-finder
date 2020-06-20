from mathematical_expression_interpreter.Symbol import Symbol
from mathematical_expression_interpreter.Result import Result
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
    char_to_symbol = {
        '+': Symbol.Addition,
        '-': Symbol.Subtraction,
        '*': Symbol.Multiplication,
        '/': Symbol.Division,
        '%': Symbol.Modulus,
        '^': Symbol.Exponential,
        'L': Symbol.Logarithm,
        '(': Symbol.OpenParenthesis,
        ')': Symbol.CloseParenthesis
    }

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    def __addition(self, a, b):
        a, b = self.__limits(a, b, bottom_result=0)
        return b + a

    def __subtraction(self, a, b):
        a, b = self.__limits(a, b, bottom_result=0)
        return b - a

    def __multiplication(self, a, b):
        a, b = self.__limits(a, b, bottom_result=0)
        return b * a

    def __division(self, a, b):
        incorrect_input = a == 0
        a, limit_reached = self.__limit(a)
        b, limit_reached = self.__limit(b, bottom_result=0)
        return b / a, incorrect_input

    def __modulus(self, a, b):
        a, b = self.__limits(a, b)
        return b % a

    def __exponential(self, a, b):
        a, limit_reached = self.__limit(a, 100, 0.01)
        if limit_reached:
            return a
        b, limit_reached = self.__limit(b)
        return pow(b, a)

    def __logarithm(self, a, b):
        incorrect_input = a == 0
        a, limit_reached = self.__limit(a, 100, 2, 100, 2)
        b, limit_reached = self.__limit(b)
        return log(a, b), incorrect_input

    def __pop(self):
        return self.numbers[-1].pop()

    def __push(self, a):
        self.numbers[-1].append(a)

    def __count(self):
        return len(self.numbers[-1])

    def __operation_pop(self):
        return self.operations[-1].pop()

    def __operation_push(self, a: Symbol):
        self.operations[-1].append(a)

    def __operation_count(self):
        return len(self.operations[-1])

    def __apply_operation(self):
        if len(self.operations) <= 0:
            return
        count = self.__count()
        if count > 1:
            operation = self.operations.pop()
            if operation == Symbol.Addition:
                self.__push(self.__addition(self.__pop(), self.__pop()))
            elif operation == Symbol.Subtraction:
                self.__push(self.__subtraction(self.__pop(), self.__pop()))
            elif operation == Symbol.Multiplication:
                self.__push(self.__multiplication(self.__pop(), self.__pop()))
            elif operation == Symbol.Division:
                res, incorrect_input = self.__division(self.__pop(), self.__pop())
                self.__push(res)
                if incorrect_input:
                    self.result = Result.DivisionByZero
            elif operation == Symbol.Modulus:
                self.__push(self.__modulus(self.__pop(), self.__pop()))
            elif operation == Symbol.Exponential:
                self.__push(self.__exponential(self.__pop(), self.__pop()))
            elif operation == Symbol.Logarithm:
                res, incorrect_input = self.__logarithm(self.__pop(), self.__pop())
                self.__push(res)
                if incorrect_input:
                    self.result = Result.LogarithmWrongInputs
            else:
                self.result = Result.WrongOperation
        else:
            self.result = Result.NumberStackWrongElements

    def __get_next_symbol(self):
        if self.pos >= len(self.expression):
            return Symbol.ExpressionEnd
        c = self.expression[self.pos]
        self.pos += 1
        expression_not_ended = True
        while type(c) is str and c.isdigit() and expression_not_ended:
            if self.pos >= len(self.expression):
                expression_not_ended = False
                c = int(c)
            else:
                c += self.expression[self.pos]
                self.pos += 1
        if type(c) is str and c[:-1].isdigit():
            c = int(c[:-1])
            self.pos -= 1
        return c

    def __limit(self, a, top_threshold=100000000000000, bottom_threshold=0.00000000001, top_result=100000000000000,
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

    def __limits(self, a, b, bottom_result=0.00000000001):
        return self.__limit(a, bottom_result=bottom_result)[0], self.__limit(b, bottom_result=bottom_result)[0]

    def __compute(self, expression):
        self.expression = ExpressionInterpreter.process_negations(expression)
        self.numbers = []
        self.numbers.append([])
        self.operations = []
        self.pos = 0
        try:
            c = self.__get_next_symbol()
            while c is not Symbol.ExpressionEnd:
                if c in self.char_to_symbol:
                    c = self.char_to_symbol[c]
                if c == Symbol.OpenParenthesis:
                    self.numbers.append([])
                elif c == Symbol.CloseParenthesis:
                    if self.__count() == 1:
                        self.__push(self.numbers.pop()[0])
                    else:
                        raise Exception
                elif c in self.char_to_symbol.values():
                    self.operations.append(c)
                else:
                    self.__push(c)
                if self.__count() == 2:
                    self.__apply_operation()
                c = self.__get_next_symbol()
        except Exception as e:
            return 0
        if len(self.numbers) <= 0 or len(self.numbers[0]) <= 0:
            a = 0
        return self.numbers[0][0]

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
    def compute(expression: str):
        ei = ExpressionInterpreter()
        return ei.__compute(expression)
