import random

from misc.config import wanted_length
from symbols.Symbol import Symbol
from symbols.interpretable_symbols.CloseParenthesis import CloseParenthesis
from symbols.interpretable_symbols.OpenParenthesis import OpenParenthesis


class Id:

    def __init__(self, symbols=None):
        self.__symbols = symbols if symbols else []

    @staticmethod
    def __random_symbol_to_append_in_list_if_not_return_random(symbols: list, prev_symbol: Symbol, exceptions: list = None):
        if not exceptions:
            exceptions = []
        symbol_lists = [symbols, Symbol.symbols()]
        valid_symbols_to_append = []
        for symbol_list in symbol_lists:
            for symbol in symbol_list:
                if symbol not in exceptions and symbol.check_prev_symbol(prev_symbol):
                    valid_symbols_to_append.append(symbol)
            if len(valid_symbols_to_append) > 0:
                return random.choice(valid_symbols_to_append)
        raise Exception

    @staticmethod
    def random(length=wanted_length):
        new_id = [Symbol.random_starting_symbol([OpenParenthesis()] if length < 6 else [])]
        last_close_parenthesis_pos = 0
        parenthesis_counter = 1 if str(new_id[-1]) == "(" else 0
        while len(new_id) < length or new_id[-1] not in Symbol.ending_symbols() or parenthesis_counter > 0:
            num_of_symbols_left_to_add = length - len(new_id)
            if parenthesis_counter > 0 and parenthesis_counter >= num_of_symbols_left_to_add:
                new_symbol = Id.__random_symbol_to_append_in_list_if_not_return_random([CloseParenthesis()], new_id[-1], [OpenParenthesis()])
            else:
                exceptions = []
                if parenthesis_counter == 0 or len(new_id) - last_close_parenthesis_pos < 3:
                    exceptions.append(CloseParenthesis())
                if num_of_symbols_left_to_add <= 4 + parenthesis_counter:
                    exceptions.append(OpenParenthesis())
                if len(new_id) + 1 >= length:
                    new_symbol = Id.__random_symbol_to_append_in_list_if_not_return_random(Symbol.ending_symbols(), new_id[-1], exceptions)
                else:
                    new_symbol = Symbol.random(new_id[-1], exceptions)
            if str(new_symbol) == "(":
                parenthesis_counter += 1
                last_close_parenthesis_pos = len(new_id)
            elif str(new_symbol) == ")":
                parenthesis_counter -= 1
            new_id.append(new_symbol)
        return Id(new_id)

    @staticmethod
    def random_connected_id():
        connected = False
        while not connected:
            new_id = str(Id.random())
            from main.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(id)
        return new_id

    def __str__(self):
        return ''.join([str(symbol) for symbol in self.__symbols])

    def __len__(self):
        return len(self.__symbols)

    def __getitem__(self, item):
        return self.__symbols[item]
