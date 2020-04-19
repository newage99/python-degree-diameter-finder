from Symbol import Symbol
from Result import Result
from math import log, pow


class ExpressionInterpreter:
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
        a = self.__limit(a)
        b = self.__limit(b, bottom_result=0)
        return b / a, incorrect_input

    def __modulus(self, a, b):
        a, b = self.__limits(a, b)
        return b % a

    def __exponential(self, a, b):
        a = self.__limit(a, 100, 0.01)
        b = self.__limit(b)
        return pow(b, a)

    def __logarithm(self, a, b):
        incorrect_input = a == 0
        a = self.__limit(a, 100, 2, 100, 2)
        b = self.__limit(b)
        return log(b, a), incorrect_input

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
            # operation = self.__operation_pop()
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

    def compute(self, expression: str):
        self.numbers = []
        self.numbers.append([])
        self.operations = []
        # self.operations.append([])
        self.expression = expression
        self.pos = 0
        try:
            c = self.__get_next_symbol()
            while c is not Symbol.ExpressionEnd:
                if c in self.char_to_symbol:
                    c = self.char_to_symbol[c]
                if c == Symbol.OpenParenthesis:
                    self.numbers.append([])
                    # self.operations.append([])
                elif c == Symbol.CloseParenthesis and self.__count() == 1:
                    self.__push(self.numbers.pop()[0])
                elif c in self.char_to_symbol.values():
                    # self.__operation_push(c)
                    self.operations.append(c)
                else:
                    self.__push(c)
                if self.__count() == 2:
                    self.__apply_operation()
                c = self.__get_next_symbol()
        except Exception as e:
            return 0
        return self.numbers[0][0]

    def __limit(self, a, top_threshold=100000000000000, bottom_threshold=0.00000000001, top_result=100000000000000,
                bottom_result=0.00000000001):
        if a > top_threshold:
            a = top_result
        elif a < -top_threshold:
            a = -top_result
        elif (bottom_threshold > a > 0) or a == 0:
            a = bottom_result
        elif -bottom_threshold < a <= 0:
            a = -bottom_result
        return a

    def __limits(self, a, b, bottom_result=0.00000000001):
        return self.__limit(a, bottom_result=bottom_result), self.__limit(b, bottom_result=bottom_result)
