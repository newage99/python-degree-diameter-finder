import random

from abc import ABC, abstractmethod
from misc.globals import get_classes_that_inherit_from


def get_symbol_folder_classes(class_they_inherit_from, function_they_implement_name: str):
    symbols = {}
    classes_that_inherit_from_symbol = None
    try:
        classes_that_inherit_from_symbol = get_classes_that_inherit_from(class_they_inherit_from, "symbols")
    except Exception as e:
        pass
    if classes_that_inherit_from_symbol:
        for obj in classes_that_inherit_from_symbol:
            if callable(getattr(obj, function_they_implement_name, None)):
                symbol = obj.symbol()
                if symbol in symbols:
                    symbols[symbol].append(obj)
                else:
                    symbols[symbol] = [obj]
        return symbols


def get_symbol_classes_that_implement_function(function_name: str = "symbol"):
    return get_symbol_folder_classes("Symbol", function_name)


class Symbol(ABC):

    __symbols_dict = None

    @staticmethod
    def symbols_dict():
        if not Symbol.__symbols_dict:
            Symbol.__symbols_dict = get_symbol_classes_that_implement_function()
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
    def choice():
        new_c = random.choice(list(Symbol.symbols_dict().keys()))
        return new_c, new_c == '(', new_c == ')'

    """
    Used on:
    check_symbol function implementations to not have to differentiate between int variables and Symbol objects.
    Subtraction has_valid_prev_char function to not have to differentiate between int variables and Symbol objects.
    """
    def __str__(self):
        return self.symbol()
