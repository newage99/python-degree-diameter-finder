import random

from abc import ABC, abstractmethod
from misc.globals import get_symbol_classes_that_inherit_from


class Symbol(ABC):

    __symbols_dict = None

    @staticmethod
    def symbols_dict():
        if not Symbol.__symbols_dict:
            Symbol.__symbols_dict = get_symbol_classes_that_inherit_from("Symbol", "symbol")
        return Symbol.__symbols_dict

    @staticmethod
    @abstractmethod
    def symbol() -> str:
        pass

    @staticmethod
    @abstractmethod
    def forbidden_prev_symbol(symbol) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def forbidden_next_symbol(symbol) -> bool:
        pass

    def check_symbol(self, char, prev_number_or_symbol):
        return char == self.symbol()

    @staticmethod
    def random():
        new_c = random.choice(list(Symbol.symbols_dict().keys()))
        return new_c, new_c == '(', new_c == ')'

    @staticmethod
    def parse(char: str, prev_number_or_symbol=None):
        symbols = Symbol.symbols_dict()
        if char in symbols:
            for symbol in symbols[char]:
                try:
                    if symbol.check_symbol(char, prev_number_or_symbol):
                        return symbol
                except Exception as e:
                    pass
        return None

    """
    Used on:
    check_symbol function implementations to not have to differentiate between int variables and Symbol objects.
    Subtraction has_valid_prev_char function to not have to differentiate between int variables and Symbol objects.
    """
    def __str__(self):
        return self.symbol()
