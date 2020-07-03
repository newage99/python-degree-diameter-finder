import random

from abc import ABC, abstractmethod
from misc.globals import get_symbol_classes_that_inherit_from


class Symbol(ABC):

    starting_symbol = True
    ending_symbol = True
    __symbols_dict = None
    __symbols_list = None
    __starting_symbols_list = None
    __ending_symbols_list = None

    # -- ABSTRACT METHODS -- #

    """
    Classes that inherit from Symbol must return the character representing them.
    """
    @staticmethod
    @abstractmethod
    def symbol() -> str:
        pass

    """
    Classes that inherit from Symbol must implement a function that checks
    if a given symbol is valid to be putted previously to themselves.
    """
    @staticmethod
    @abstractmethod
    def forbidden_prev_symbol(symbol) -> bool:
        pass

    """
    Classes that inherit from Symbol must implement a function that checks
    if a given symbol is valid to be putted next to themselves.
    """
    @staticmethod
    @abstractmethod
    def forbidden_next_symbol(symbol) -> bool:
        pass

    # -- PRIVATE STATIC METHODS -- #

    @staticmethod
    def __create_symbol_list(list_to_create, variable_name_that_must_be_true: str):
        if not list_to_create:
            list_to_create = []
            symbols_dict = Symbol.symbols_dict()
            for dict in symbols_dict:
                for symbol in symbols_dict[dict]:
                    if getattr(symbol, variable_name_that_must_be_true, False):
                        list_to_create.append(symbol)
            return list_to_create

    # -- STATIC METHODS -- #

    @staticmethod
    def symbols_dict():
        if not Symbol.__symbols_dict:
            Symbol.__symbols_dict = get_symbol_classes_that_inherit_from("Symbol", "symbol")
        return Symbol.__symbols_dict

    @staticmethod
    def symbols():
        if not Symbol.__symbols_list:
            Symbol.__symbols_list = []
            symbols_dict = Symbol.symbols_dict()
            for value in symbols_dict.values():
                Symbol.__symbols_list += value
        return Symbol.__symbols_list

    @staticmethod
    def starting_symbols() -> list:
        return Symbol.__create_symbol_list(Symbol.__starting_symbols_list, "starting_symbol")

    @staticmethod
    def ending_symbols() -> list:
        return Symbol.__create_symbol_list(Symbol.__ending_symbols_list, "ending_symbol")

    @staticmethod
    def random_starting_symbol(exceptions=None):
        symbols_to_choose_from = []
        if not exceptions:
            exceptions = []
        for symbol in Symbol.starting_symbols():
            if symbol not in exceptions:
                symbols_to_choose_from.append(symbol)
        new_symbol = random.choice(symbols_to_choose_from)
        return new_symbol

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

    @staticmethod
    def random(prev_symbol=None, exceptions=None):
        if exceptions is None:
            exceptions = []
        symbols_to_choose_from = []
        for symbol in Symbol.symbols():
            if symbol not in exceptions and (not prev_symbol or symbol.check_prev_symbol(prev_symbol)):
                symbols_to_choose_from.append(symbol)
        return random.choice(symbols_to_choose_from)

    # -- INSTANCE METHODS -- #

    def check_symbol(self, char, prev_num_or_symb):
        return char == self.symbol() and (self.starting_symbol or prev_num_or_symb) and not self.forbidden_prev_symbol(
            prev_num_or_symb)

    def check_prev_symbol(self, prev):
        return prev and not self.forbidden_prev_symbol(prev) and not prev.forbidden_next_symbol(self)

    # -- MAGIC METHODS OVERRIDES -- #

    def __str__(self):
        return self.symbol()

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__
