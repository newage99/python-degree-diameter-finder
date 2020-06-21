from abc import ABC, abstractmethod


class Symbol(ABC):

    @staticmethod
    @abstractmethod
    def symbol():
        pass

    @abstractmethod
    def process(self):
        pass

    def check_symbol(self, char, prev_char):
        return char == self.symbol()

    # Used on check_symbol functions in order to not having to differentiate between int variables and Symbol objects.
    def __str__(self):
        return self.symbol()
