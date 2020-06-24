from abc import abstractmethod
from symbols.Symbol import Symbol, get_symbol_classes_that_implement_function


class InterpretableSymbol(Symbol):

    __interpretable_symbols_dict = None

    @staticmethod
    def interpretable_symbols_dict():
        if not InterpretableSymbol.__interpretable_symbols_dict:
            InterpretableSymbol.__interpretable_symbols_dict = get_symbol_classes_that_implement_function("interpret")
        return InterpretableSymbol.__interpretable_symbols_dict

    @abstractmethod
    def interpret(self):
        pass
