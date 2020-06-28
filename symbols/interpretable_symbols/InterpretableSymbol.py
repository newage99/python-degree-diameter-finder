from abc import abstractmethod
from misc.globals import get_symbol_classes_that_inherit_from
from symbols.Symbol import Symbol


class InterpretableSymbol(Symbol):

    __interpretable_symbols_dict = None

    @staticmethod
    def interpretable_symbols_dict():
        if not InterpretableSymbol.__interpretable_symbols_dict:
            InterpretableSymbol.__interpretable_symbols_dict = get_symbol_classes_that_inherit_from(
                "InterpretableSymbol", "interpret")
        return InterpretableSymbol.__interpretable_symbols_dict

    @abstractmethod
    def interpret(self):
        pass
