import random

from misc.Random import random_bool
from misc.config import wanted_length
from symbols.Symbol import Symbol
from symbols.interpretable_symbols.CloseParenthesis import CloseParenthesis
from symbols.interpretable_symbols.OpenParenthesis import OpenParenthesis
from symbols.interpretable_symbols.functions.Function import Function
from symbols.numbers.Number import Number


class Id:

    def __init__(self, symbols=None):
        self.__symbols = symbols if symbols else []
        self.__initial_length = len(self.__symbols)

    # -- PRIVATE METHODS -- #

    # @staticmethod
    # def __set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix):
    #     symbol_to_set = Number.random() if var_or_operator else Operator.random()
    #     return (None, symbol_to_set) if suffix_or_prefix else (symbol_to_set, None)
    #
    # def __get_symbols_available_to_mutate_to(self, pos_to_mutate):
    #     prev_symbol = self[pos_to_mutate - 1] if pos_to_mutate > 0 else None
    #     next_symbol = self[pos_to_mutate + 1] if pos_to_mutate + 1 < len(self) else None
    #     symbols_available_to_mutate_to = Symbol.symbols().copy()
    #     char_to_mutate = str(self[pos_to_mutate])
    #
    #     # if char_to_mutate != "(" and char_to_mutate != ")":
    #     for symbol in Symbol.symbols():
    #         if (prev_symbol and not Symbol.check(prev_symbol, symbol)) or (
    #                 not prev_symbol and not symbol.starting_symbol) or (
    #                 next_symbol and not Symbol.check(symbol, next_symbol)) or (
    #                 not next_symbol and not symbol.ending_symbol):
    #             symbols_available_to_mutate_to.remove(symbol)
    #     if len(symbols_available_to_mutate_to) == 0:
    #         raise Exception
    #
    #     if self[pos_to_mutate] in symbols_available_to_mutate_to:
    #         symbols_available_to_mutate_to.remove(self[pos_to_mutate])
    #
    #     if (char_to_mutate == '(' or self.__is_not_worth_mutate_to_close_parenthesis(
    #             pos_to_mutate)) and CloseParenthesis() in symbols_available_to_mutate_to:
    #         # If char to mutate is '(' or if we are to close to the beginning of the id or to a '(' char,
    #         # is not worth to mutate to char ')'.
    #         symbols_available_to_mutate_to.remove(CloseParenthesis())
    #     if (char_to_mutate == ')' or self.__is_not_worth_mutate_to_open_parenthesis(
    #             pos_to_mutate)) and OpenParenthesis() in symbols_available_to_mutate_to:
    #         # If char to mutate is ')' or if we are to close to the end of the id or to a ')' char,
    #         # is not worth to mutate to char ')'.
    #         symbols_available_to_mutate_to.remove(OpenParenthesis())
    #
    #     return symbols_available_to_mutate_to
    #
    # def __clean_symbol_to_mutate_to(self, pos_to_mutate: int, symbol_to_mutate_to: Symbol):
    #     prefix = None
    #     suffix = None
    #     symbol_to_mutate = self[pos_to_mutate]
    #     prev_symbol = self[pos_to_mutate - 1] if pos_to_mutate > 0 else None
    #     next_symbol = self[pos_to_mutate + 1] if pos_to_mutate + 1 < len(self) else None
    #
    #     if (str(symbol_to_mutate) == "(" or str(symbol_to_mutate) == ")") and len(self) > self.__initial_length:
    #         if Symbol.check(prev_symbol, next_symbol):
    #             symbol_to_mutate_to = None
    #         else:
    #             symbols_to_replace_symbol_to_mutate_to = []
    #             for symbol in Symbol.symbols():
    #                 if Symbol.check(prev_symbol, symbol) and Symbol.check(symbol, next_symbol) and str(
    #                         symbol) != "(" and str(symbol) != ")":
    #                     symbols_to_replace_symbol_to_mutate_to.append(symbol)
    #             if len(symbols_to_replace_symbol_to_mutate_to) > 0:
    #                 symbol_to_mutate_to = random.choice(symbols_to_replace_symbol_to_mutate_to)
    #             else:
    #                 raise Exception
    #
    #     final_symbols = []
    #     if prefix:
    #         final_symbols.append(prefix)
    #     if symbol_to_mutate_to:
    #         final_symbols.append(symbol_to_mutate_to)
    #     if suffix:
    #         final_symbols.append(suffix)
    #
    #     return final_symbols

    @staticmethod
    def __insert_open_parenthesis_until_pos(id, pos):
        positions_to_insert_open_parenthesis = []
        while pos >= 0:
            prev_symbol = id[pos - 1] if pos > 0 else None
            if str(id[pos]) == ')':
                pos -= 3
            elif (not prev_symbol or (isinstance(prev_symbol, Function) or str(prev_symbol) == "(")) and (
                        isinstance(id[pos], Number) or str(id[pos]) == "("):
            # elif (prev_char in (Operator.operators() + "(") or prev_char == '') and id[pos] in (numbers + "("):
                positions_to_insert_open_parenthesis.append(pos)
            pos -= 1
        there_are_positions_to_insert_open_parenthesis = len(positions_to_insert_open_parenthesis) > 0
        if there_are_positions_to_insert_open_parenthesis:
            pos = random.choice(positions_to_insert_open_parenthesis)
            return Id(id[:pos] + [OpenParenthesis()] + id[pos:])
        raise Exception

    @staticmethod
    def __insert_close_parenthesis_from_pos(id, pos):
        positions_to_insert_close_parenthesis = []
        len_id = len(id)
        while pos < len_id:
            prev_symbol = id[pos - 1] if pos > 0 else None
            if str(id[pos]) == '(':
                pos += 3

            elif (prev_symbol and (isinstance(prev_symbol, Number) or str(prev_symbol) == ")")) and (
                        isinstance(id[pos], Function) or str(id[pos]) == ")"):
            # elif prev_char in (numbers + ")") and id[pos] in (Operator.operators() + ")"):
                positions_to_insert_close_parenthesis.append(pos)
            pos += 1
        positions_to_insert_close_parenthesis.append(len_id)
        pos = random.choice(positions_to_insert_close_parenthesis)
        if pos == len_id:
            return Id(id + CloseParenthesis())
        return Id(id[:pos] + [CloseParenthesis()] + id[pos:])

    @staticmethod
    def __add_parenthesis_if_needed(id):
        parenthesis_inserted = True
        while parenthesis_inserted:
            parenthesis_inserted = False
            parenthesis_counter = 0
            for i in range(len(id)):
                char = str(id[i])
                if char == '(':
                    parenthesis_counter += 1
                elif char == ')':
                    if parenthesis_counter == 0:
                        id = Id.__insert_open_parenthesis_until_pos(id, i - 3)
                        parenthesis_inserted = True
                        break
                    else:
                        parenthesis_counter -= 1
            # This means there has been one or more open parenthesis not closed.
            if not parenthesis_inserted and parenthesis_counter > 0:
                id = Id.__insert_close_parenthesis_from_pos(id, str(id).rfind('(') + 4)
                parenthesis_inserted = True
        return id

    @staticmethod
    def __remove_open_parenthesis(id):
        positions_to_remove_open_parenthesis = []
        len_id = len(id)
        parenthesis_counter = 0
        pos = len(id) - 1
        while pos >= 0:
            if str(id[pos]) == "(":
                parenthesis_counter += 1
            elif str(id[pos]) == ")":
                parenthesis_counter -= 1
            if parenthesis_counter > 0:
                break
            pos -= 1
        while pos < len_id:
            prev_symbol = id[pos - 1] if pos > 0 else None
            next_symbol = id[pos + 1] if pos + 1 < len(id) else None
            if str(id[pos]) == "(":
                parenthesis_counter += 1
                if not prev_symbol or Symbol.check(prev_symbol, next_symbol):
                    positions_to_remove_open_parenthesis.append(pos)
            elif str(id[pos]) == ")":
                parenthesis_counter -= 1
            if parenthesis_counter == 0:
                break
            pos += 1
        if len(positions_to_remove_open_parenthesis) > 0:
            pos_to_remove = random.choice(positions_to_remove_open_parenthesis)
            return Id(id[:pos_to_remove] + id[pos_to_remove + 1:])
        raise Exception

    @staticmethod
    def __remove_close_parenthesis_until_pos(id, pos):
        positions_to_remove_close_parenthesis = []
        while pos >= 0:
            prev_symbol = id[pos - 1] if pos > 0 else None
            next_symbol = id[pos + 1] if pos + 1 < len(id) else None
            if str(id[pos]) == ")" and (not next_symbol or Symbol.check(prev_symbol, next_symbol)):
                positions_to_remove_close_parenthesis.append(pos)
            pos -= 1
        if len(positions_to_remove_close_parenthesis) > 0:
            pos_to_remove = random.choice(positions_to_remove_close_parenthesis)
            return Id(id[:pos_to_remove] + id[pos_to_remove + 1:])
        raise Exception

    @staticmethod
    def __remove_parenthesis_if_needed(id):
        parenthesis_removed = True
        while parenthesis_removed:
            parenthesis_removed = False
            parenthesis_counter = 0
            for i in range(len(id)):
                char = str(id[i])
                if char == '(':
                    parenthesis_counter += 1
                elif char == ')':
                    if parenthesis_counter == 0:
                        id = Id.__remove_close_parenthesis_until_pos(id, i)
                        parenthesis_removed = True
                        break
                    else:
                        parenthesis_counter -= 1
            if not parenthesis_removed and parenthesis_counter > 0:
                id = Id.__remove_open_parenthesis(id)
                parenthesis_removed = True
        return id

    @staticmethod
    def __add_or_remove_parenthesis_if_needed(id):
        if len(id) > id.__initial_length or (len(id) == id.__initial_length and random_bool()):
            return Id.__remove_parenthesis_if_needed(id)
        else:
            return Id.__add_parenthesis_if_needed(id)

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

    # -- PUBLIC METHODS -- #

    @staticmethod
    def random(length=wanted_length):
        new_id = [Symbol.random_starting_symbol([OpenParenthesis()] if length < 6 else [])]
        last_close_parenthesis_pos = 0
        parenthesis_counter = 1 if str(new_id[-1]) == "(" else 0
        while len(new_id) < length or new_id[-1] not in Symbol.ending_symbols() or parenthesis_counter > 0:
            num_of_symbols_left_to_add = length - len(new_id)
            symbols = []
            exceptions = []
            if parenthesis_counter > 0 and parenthesis_counter >= num_of_symbols_left_to_add:
                symbols = [CloseParenthesis()]
                exceptions = [OpenParenthesis()]
            else:
                if parenthesis_counter == 0 or len(new_id) - last_close_parenthesis_pos < 3:
                    exceptions.append(CloseParenthesis())
                if num_of_symbols_left_to_add <= 4 + parenthesis_counter:
                    exceptions.append(OpenParenthesis())
                if len(new_id) + 1 >= length:
                    symbols = Symbol.ending_symbols()
            new_symbol = Symbol.random(new_id[-1], exceptions, symbols, True)
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

    def __replace_symbol_at_random_pos(self, additional_data: bool = False):

        length = len(self)
        pos = random.choice(range(length))
        prev_symbol = self[pos - 1] if pos > 0 else None
        next_symbol = self[pos + 1] if pos + 1 < length else None
        worth_mutate_to_open = not self.__is_not_worth_mutate_to_open_parenthesis(pos)
        worth_mutate_to_close = not self.__is_not_worth_mutate_to_close_parenthesis(pos)
        symbols = Symbol.symbols().copy().remove(self[pos])
        symbols_to_mutate_to = []

        for symbol in Symbol.symbols():
            char = str(symbol)
            if ((char != "(" and char != ")") or (
                    (char == "(" and worth_mutate_to_open) or (char == ")" and worth_mutate_to_close))):
                if symbol != self[pos] and Symbol.check(prev_symbol, symbol) and Symbol.check(symbol, next_symbol):
                    symbols_to_mutate_to.append(symbol)
            else:
                symbols.remove(symbol)

        if len(symbols_to_mutate_to) > 0:
            return Id(self.__symbols[:pos] + [random.choice(symbols_to_mutate_to)] + self.__symbols[pos+1:])
        else:

            prev_prev = self[pos - 2] if pos > 1 else None
            next_next = self[pos + 2] if pos + 2 < length else None
            final_symbols = []

            for symbol1 in symbols:
                for symbol2 in symbols:
                    if Symbol.check(symbol1, symbol2):
                        if Symbol.check(prev_prev, symbol1) and Symbol.check(symbol2, next_symbol):
                            final_symbols.append([symbol1, symbol2, next_symbol] if next_symbol else [symbol1, symbol2])
                        if Symbol.check(prev_symbol, symbol1) and Symbol.check(symbol2, next_next):
                            final_symbols.append([prev_symbol, symbol1, symbol2] if prev_symbol else [symbol1, symbol2])

            if len(final_symbols) == 0:
                raise Exception

            final_symbol_list = random.choice(final_symbols)
            beginning = self.__symbols[:pos-(1 if prev_symbol else 0)]
            ending = self.__symbols[pos+(1 if next_symbol else 0)]
            new_id = Id(beginning + final_symbol_list + ending)
            if additional_data:
                return new_id, pos, str(self[pos]), str(final_symbol_list)
            return new_id

    def mutate(self, additional_data: bool = False):

        if additional_data:
            new_id, pos, char_to_mutate, char_to_mutate_to = self.__replace_symbol_at_random_pos(additional_data)
        else:
            new_id = self.__replace_symbol_at_random_pos()
        new_id = Id.__add_or_remove_parenthesis_if_needed(new_id)
        if additional_data:
            return new_id, pos, char_to_mutate, char_to_mutate_to
        return new_id

    # -- MAGIC METHODS OVERRIDES -- #

    def __str__(self):
        return ''.join([str(symbol) for symbol in self.__symbols])

    def __len__(self):
        return len(self.__symbols)

    def __getitem__(self, item):
        return self.__symbols[item]

    def __add__(self, other):
        if other is None:
            return Id(self.__symbols)
        else:
            class_name = other.__class__.__name__
            if class_name == "Id":
                return Id(self.__symbols + other.__symbols)
            elif isinstance(other, Symbol):
                return Id(self.__symbols + [other])
        return None
