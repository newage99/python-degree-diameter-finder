from abc import abstractmethod
from misc.globals import get_symbol_classes_that_inherit_from
from symbols.Symbol import Symbol


class InterpretableSymbol(Symbol):

    __interpretable_symbols_dict = None
    __symbols_list = None

    @staticmethod
    def symbols():
        if not InterpretableSymbol.__symbols_list:
            symbols_dict = get_symbol_classes_that_inherit_from("InterpretableSymbol", "symbol")
            for value in symbols_dict.values():
                InterpretableSymbol.__symbols_list += value
        return InterpretableSymbol.__symbols_list

    @staticmethod
    def interpretable_symbols_dict():
        if not InterpretableSymbol.__interpretable_symbols_dict:
            InterpretableSymbol.__interpretable_symbols_dict = get_symbol_classes_that_inherit_from(
                "InterpretableSymbol", "interpret")
        return InterpretableSymbol.__interpretable_symbols_dict

    @staticmethod
    def random(prev_symbol=None, exceptions=None, symbols=None):
        from symbols.Symbol import Symbol
        return Symbol.random(prev_symbol, exceptions, InterpretableSymbol.symbols())

    @abstractmethod
    def interpret(self):
        pass
