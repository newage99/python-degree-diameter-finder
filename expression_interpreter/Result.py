from enum import Enum


class Result(Enum):
    OK = 1
    DivisionByZero = 2
    ModulusOnZero = 3
    ExponentWrongInputs = 4
    LogarithmWrongInputs = 5
    FactorWrongSymbol = 6
    CloseParenthesisMissing = 7
    GetNextSymbolWrongSymbol = 8
    NumberStackWrongElements = 9
    WrongOperation = 10
    CloseParenthesisWrongStructure = 11
