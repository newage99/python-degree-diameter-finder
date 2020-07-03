import random

from misc.config import wanted_length
from symbols.Symbol import Symbol
from symbols.interpretable_symbols.CloseParenthesis import CloseParenthesis
from symbols.interpretable_symbols.OpenParenthesis import OpenParenthesis


class Id:

    def __init__(self, symbols=None):
        self.__symbols = symbols if symbols else []

    # -- PRIVATE METHODS -- #

    @staticmethod
    def __random_symbol_to_append_in_list_if_not_return_random(symbols: list, prev_symbol: Symbol,
                                                               exceptions: list = None):
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

    def __is_not_worth_mutate_to_open_parenthesis(self, pos_to_mutate):
        len_id = len(self.__symbols)
        pos_to_mutate_plus_four = pos_to_mutate + 4
        if pos_to_mutate_plus_four >= len_id:
            return True
        else:
            pos = pos_to_mutate + 1
            while pos < pos_to_mutate_plus_four:
                if str(self.__symbols[pos]) == ')':
                    return True
                pos += 1
        return False

    def __is_not_worth_mutate_to_close_parenthesis(self, pos_to_mutate):
        if pos_to_mutate < 4:
            return True
        else:
            pos_to_mutate_minus_four = pos_to_mutate - 4
            pos = pos_to_mutate - 1
            while pos > pos_to_mutate_minus_four:
                if str(self.__symbols[pos]) == '(':
                    return True
                pos -= 1
        return False

    def __get_symbols_available_to_mutate_to(self, pos_to_mutate):
        true_and_false_list = [True, False]
        forbidden_symbols = []
        pos_to_mutate = str(self).find('(')
        for boolean in true_and_false_list:
            for symbol in Symbol.symbols():
                if pos_to_mutate > 0 if boolean else pos_to_mutate + 1 < len(self.__symbols):
                    symbol_to_check = self.__symbols[pos_to_mutate + (-1 if boolean else 1)]
                    if symbol_to_check.forbidden_next_symbol(
                            symbol_to_check) if boolean else symbol_to_check.forbidden_prev_symbol(symbol_to_check):
                        forbidden_symbols.append(symbol)
                elif (not symbol.starting_symbol if boolean else not symbol.ending_symbol) and symbol not in forbidden_symbols:
                    forbidden_symbols.append(symbol)
        symbols_available_to_mutate_to = []
        for symbol in Symbol.symbols():
            if symbol not in forbidden_symbols and symbol != self.__symbols[pos_to_mutate]:
                symbols_available_to_mutate_to.append(symbol)
        char_to_mutate = str(self.__symbols[pos_to_mutate])
        if (char_to_mutate == '(' or self.__is_not_worth_mutate_to_close_parenthesis(
                pos_to_mutate)) and CloseParenthesis() in symbols_available_to_mutate_to:
            # If char to mutate is '(' or if we are to close to the beginning of the id or to a '(' char,
            # is not worth to mutate to char ')'.
            symbols_available_to_mutate_to.remove(CloseParenthesis())
        if (char_to_mutate == ')' or self.__is_not_worth_mutate_to_open_parenthesis(
                pos_to_mutate)) and OpenParenthesis() in symbols_available_to_mutate_to:
            # If char to mutate is ')' or if we are to close to the end of the id or to a ')' char,
            # is not worth to mutate to char ')'.
            symbols_available_to_mutate_to.remove(OpenParenthesis())
        return symbols_available_to_mutate_to

    def __clean_symbol_to_mutate_to(self, symbol_to_mutate_to):
        pass

    # -- PUBLIC METHODS -- #

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

    def mutate(self):
        symbols_available_to_mutate_to = []
        pos_to_mutate = -1
        while len(symbols_available_to_mutate_to) == 0:
            pos_to_mutate = random.randint(0, len(self.__symbols) - 1)
            symbols_available_to_mutate_to = self.__get_symbols_available_to_mutate_to(pos_to_mutate)
        symbol_to_mutate_to = random.choice(symbols_available_to_mutate_to)
        prefix, symbol_to_mutate_to, suffix = self.__clean_symbol_to_mutate_to(symbol_to_mutate_to)
        new_id = self.__symbols[:pos_to_mutate] + prefix + symbol_to_mutate_to + suffix + self.__symbols[pos_to_mutate + 1:]
        return new_id

    # -- MAGIC METHODS OVERRIDES -- #

    def __str__(self):
        return ''.join([str(symbol) for symbol in self.__symbols])

    def __len__(self):
        return len(self.__symbols)

    def __getitem__(self, item):
        return self.__symbols[item]

    def __add__(self, other):
        return Id(self.__symbols + other.__symbols)


if __name__ == "__main__":
    id = Id.random(10)
    while "(" not in str(id):
        id = Id.random(10)
    id.mutate()
