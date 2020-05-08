from enum import Enum


class Symbol(Enum):
    Default = 0
    Number = 1
    Addition = 2
    Subtraction = 3
    Multiplication = 4
    Division = 5
    Modulus = 6
    Exponential = 7
    Logarithm = 8
    OpenParenthesis = 9
    CloseParenthesis = 10
    ExpressionEnd = 11
