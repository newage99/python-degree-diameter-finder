from abc import ABC, abstractmethod


class Symbol(ABC):

    @abstractmethod
    def symbol(self):
        pass

    @abstractmethod
    def process(self):
        pass

    def check_symbol(self, char, prev_char):
        return char == self.symbol()
