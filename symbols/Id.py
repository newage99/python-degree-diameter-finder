import random

from misc.Random import random_bool
from misc.config import wanted_length
from symbols.Symbol import Symbol
from symbols.interpretable_symbols.CloseParenthesis import CloseParenthesis
from symbols.interpretable_symbols.OpenParenthesis import OpenParenthesis
from symbols.interpretable_symbols.functions.Function import Function
from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction
from symbols.numbers.Number import Number


class Id:

    def __init__(self, symbols=None, initial_length: int = None):
        self.__symbols = symbols if symbols else []
        self.__initial_length = initial_length if initial_length else len(self.__symbols)

    # -- PRIVATE METHODS -- #

    @staticmethod
    def __insert_open_or_remove_close_parenthesis_until_pos(id, initial_pos, insert_or_remove: bool):
        positions = []
        pos = initial_pos
        while pos >= 0:
            prev_symbol = id[pos - 1] if pos > 0 else None
            next_symbol = id[pos + 1] if pos + 1 < len(id) else None
            if insert_or_remove and str(id[pos]) == ")":
                pos -= 3
            elif (insert_or_remove and (
                        not prev_symbol or (isinstance(prev_symbol, Function) or str(prev_symbol) == "(")) and (
                              isinstance(id[pos], Number) or isinstance(id[pos], SingleArgFunction) or str(
                          id[pos]) == "(")) or (not insert_or_remove and (
                        str(id[pos]) == ")" and (not next_symbol or Symbol.check(prev_symbol, next_symbol)))):
                positions.append(pos)
            pos -= 1
        if len(positions) > 0:
            pos = random.choice(positions)
            return Id(id[:pos] + ([OpenParenthesis()] + id[pos:] if insert_or_remove else id[pos + 1:]),
                      id.__initial_length)
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
                positions_to_insert_close_parenthesis.append(pos)
            pos += 1
        positions_to_insert_close_parenthesis.append(len_id)
        pos = random.choice(positions_to_insert_close_parenthesis)
        new_id = Id(id[:pos] + [CloseParenthesis()] + id[pos:], id.__initial_length)
        return new_id

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
        conflicting_open_parenthesis_positions = []
        while pos < len_id:
            prev_symbol = id[pos - 1] if pos > 0 else None
            next_symbol = id[pos + 1] if pos + 1 < len(id) else None
            if str(id[pos]) == "(":
                parenthesis_counter += 1
                if not prev_symbol or Symbol.check(prev_symbol, next_symbol):
                    positions_to_remove_open_parenthesis.append(pos)
                else:
                    conflicting_open_parenthesis_positions.append(pos)
            elif str(id[pos]) == ")":
                parenthesis_counter -= 1
            if parenthesis_counter == 0:
                break
            pos += 1
        if len(positions_to_remove_open_parenthesis) > 0:
            pos_to_remove = random.choice(positions_to_remove_open_parenthesis)
            return Id(id[:pos_to_remove] + id[pos_to_remove + 1:], id.__initial_length)
        elif len(conflicting_open_parenthesis_positions) > 0:
            new_id = id.copy()
            for pos in conflicting_open_parenthesis_positions:
                new_id = new_id.__mutate(pos, False)
            return new_id
        raise Exception

    @staticmethod
    def __add_or_remove_parenthesis_if_needed(id):
        add_or_remove = len(id) < id.__initial_length or (len(id) == id.__initial_length and random_bool())
        parenthesis_managed = True
        new_id = id.copy()
        while parenthesis_managed:
            parenthesis_managed = False
            parenthesis_counter = 0
            for i in range(len(new_id)):
                char = str(new_id[i])
                if char == '(':
                    parenthesis_counter += 1
                elif char == ')':
                    if parenthesis_counter == 0:
                        new_id = Id.__insert_open_or_remove_close_parenthesis_until_pos(new_id,
                                                                                        i - (3 if add_or_remove else 0),
                                                                                        add_or_remove)
                        parenthesis_managed = True
                        break
                    else:
                        parenthesis_counter -= 1
            if not parenthesis_managed and parenthesis_counter > 0:
                if add_or_remove:
                    new_id = Id.__insert_close_parenthesis_from_pos(new_id, str(new_id).rfind('(') + 4)
                else:
                    new_id = Id.__remove_open_parenthesis(new_id)
                parenthesis_managed = True
        return new_id

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
        return Id(new_id, length)

    @staticmethod
    def random_connected_id():
        connected = False
        while not connected:
            new_id = str(Id.random())
            from main.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(id)
        return new_id

    def __remove_symbol_at_pos(self, pos: int, additional_data: bool = False):
        pass

    def __insert_symbol_at_pos(self, pos: int, additional_data: bool = False):
        pass

    def __manage_symbol_at_pos(self, pos: int, additional_data: bool = False):
        equal = len(self) == self.__initial_length
        bigger = len(self) > self.__initial_length
        length = len(self)
        prev_symbol = self[pos - 1] if pos > 0 else None
        next_symbol = self[pos + 1] if pos + 1 < length else None
        prev_prev = self[pos - 2] if pos > 1 else None
        next_next = self[pos + 2] if pos + 2 < length else None
        symbols = Symbol.symbols().copy()
        symbols.remove(self[pos])
        if OpenParenthesis() in symbols and self.__is_not_worth_mutate_to_open_parenthesis(pos):
            symbols.remove(OpenParenthesis())
        if CloseParenthesis() in symbols and self.__is_not_worth_mutate_to_close_parenthesis(pos):
            symbols.remove(CloseParenthesis())

        if bigger and Symbol.check(prev_symbol, next_symbol):
            new_id = Id(self[:pos] + self[pos + 1:], self.__initial_length)
            if additional_data:
                return new_id, pos, str(self[pos]), 'None'
            return new_id
        else:
            symbols_to_mutate_to = []
            for symbol in symbols:
                if bigger:
                    if Symbol.check(prev_prev, symbol) and Symbol.check(symbol, next_symbol):
                        symbols_to_mutate_to.append([symbol, next_symbol] if next_symbol else [symbol])
                    elif Symbol.check(prev_symbol, symbol) and Symbol.check(symbol, next_next):
                        symbols_to_mutate_to.append([prev_symbol, symbol] if prev_symbol else [symbol])
                elif Symbol.check(prev_symbol, symbol) and Symbol.check(symbol, next_symbol if equal else self[pos]):
                    symbols_to_mutate_to.append([symbol])
            if len(symbols_to_mutate_to) > 0:
                symbols_to_mutate_to = random.choice(symbols_to_mutate_to)
                ending = self[pos + (2 if bigger else (1 if equal else 0)):]
                beginning = self[:pos-(1 if bigger and pos > 0 else 0)]
                new_id = Id(beginning + symbols_to_mutate_to + ending, self.__initial_length)
                if additional_data:
                    return new_id, pos, str(self[pos]), str([str(s) for s in symbols_to_mutate_to])
                return new_id
            elif bigger:
                raise Exception
            else:

                final_symbols = []
                last_s = next_symbol if equal else self[pos]
                first_s = prev_symbol if equal else self[pos]

                for s1 in symbols:
                    for s2 in symbols:
                        if Symbol.check(s1, s2):
                            if Symbol.check(prev_prev if equal else prev_symbol, s1) and Symbol.check(s2, last_s):
                                final_symbols.append([s1, s2, last_s] if next_symbol else [s1, s2])
                            if Symbol.check(first_s, s1) and Symbol.check(s2, next_next if equal else next_symbol):
                                final_symbols.append([first_s, s1, s2] if prev_symbol else [s1, s2])

                if len(final_symbols) == 0:
                    raise Exception

                final_symbol_list = random.choice(final_symbols)
                new_id = Id(self[:pos - (1 if equal else 0)] + final_symbol_list + self[pos + (2 if equal else 1):],
                            self.__initial_length)
                if additional_data:
                    return new_id, pos, str(self[pos]), str([str(s) for s in final_symbol_list])
                return new_id

    def __mutate(self, pos, additional_data: bool):
        if additional_data:
            unchecked_id, pos, char_to_mutate, char_to_mutate_to = self.__manage_symbol_at_pos(pos, additional_data)
        else:
            unchecked_id = self.__manage_symbol_at_pos(pos)
        new_id = Id.__add_or_remove_parenthesis_if_needed(unchecked_id)
        if additional_data:
            return new_id, pos, char_to_mutate, char_to_mutate_to
        return new_id

    def mutate(self, additional_data: bool = False):
        pos = random.choice(range(len(self)))
        return self.__mutate(pos, additional_data)

    # -- MAGIC METHODS OVERRIDES -- #

    def copy(self):
        return Id(self.__symbols.copy(), self.__initial_length)

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return ''.join([str(symbol) for symbol in self.__symbols])

    def __len__(self):
        return len(self.__symbols)

    def __getitem__(self, item):
        return self.__symbols[item]

    def __add__(self, other):
        if other is None:
            return Id(self.__symbols, self.__initial_length)
        else:
            class_name = other.__class__.__name__
            if class_name == "Id":
                return Id(self.__symbols + other.__symbols, self.__initial_length)
            elif isinstance(other, Symbol):
                return Id(self.__symbols + [other], self.__initial_length)
        return None
