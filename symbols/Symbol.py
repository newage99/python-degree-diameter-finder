from abc import ABC, abstractmethod


class Symbol(ABC):

    @staticmethod
    @abstractmethod
    def symbol():
        pass

    @abstractmethod
    def process(self):
        pass

    def check_symbol(self, char, prev_number_or_symbol):
        return char == self.symbol()

    """
    Used on:
    check_symbol function implementations to not have to differentiate between int variables and Symbol objects.
    Subtraction has_valid_prev_char function to not have to differentiate between int variables and Symbol objects.
    """
    # Used on
    def __str__(self):
        return self.symbol()
