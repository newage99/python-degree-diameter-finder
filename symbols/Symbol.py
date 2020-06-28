import random

from abc import ABC, abstractmethod
from misc.globals import get_symbol_classes_that_inherit_from


class Symbol(ABC):

    starting_symbol = True
    ending_symbol = True

    __symbols_dict = None

    @staticmethod
    def symbols_dict():
        if not Symbol.__symbols_dict:
            Symbol.__symbols_dict = get_symbol_classes_that_inherit_from("Symbol", "symbol")
        return Symbol.__symbols_dict

    @staticmethod
    def create_symbol_list(list_to_create, variable_name_that_must_be_true: str):
        if not list_to_create:
            list_to_create = []
            symbols_dict = Symbol.symbols_dict()
            for dict in symbols_dict:
                for symbol in symbols_dict[dict]:
                    if getattr(symbol, variable_name_that_must_be_true, False) and symbol.symbol() not in list_to_create:
                        list_to_create.append(symbol.symbol())
            return list_to_create

    __starting_symbols_list = None

    @staticmethod
    def starting_symbols() -> list:
        return Symbol.create_symbol_list(Symbol.__starting_symbols_list, "starting_symbol")

    __ending_symbols_list = None

    @staticmethod
    def ending_symbols() -> list:
        return Symbol.create_symbol_list(Symbol.__ending_symbols_list, "ending_symbol")

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

    def check_symbol(self, char, prev_num_or_symb):
        return char == self.symbol() and (self.starting_symbol or prev_num_or_symb) and not self.forbidden_prev_symbol(
            prev_num_or_symb)

    @staticmethod
    def random():
        new_c = random.choice(list(Symbol.symbols_dict().keys()))
        return new_c, new_c == '(', new_c == ')'

    @staticmethod
    def random_starting_symbol():
        new_c = random.choice(Symbol.starting_symbols())
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
