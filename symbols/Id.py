import random

from misc.Random import random_bool
from misc.config import wanted_length
from symbols.Symbol import Symbol
from symbols.interpretable_symbols.CloseParenthesis import CloseParenthesis
from symbols.interpretable_symbols.OpenParenthesis import OpenParenthesis
from symbols.interpretable_symbols.functions.Function import Function
from symbols.interpretable_symbols.functions.operators.Operator import Operator
from symbols.interpretable_symbols.functions.single_arg_functions.SingleArgFunction import SingleArgFunction
from symbols.numbers.Number import Number


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

    @staticmethod
    def __set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix):
        symbol_to_set = Number.random() if var_or_operator else Operator.random()
        return (None, symbol_to_set) if suffix_or_prefix else (symbol_to_set, None)

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
            pos = positions_to_insert_open_parenthesis[random.randint(0, len(positions_to_insert_open_parenthesis) - 1)]
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
        pos = positions_to_insert_close_parenthesis[random.randint(0, len(positions_to_insert_close_parenthesis) - 1)]
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
        char_to_mutate = str(self[pos_to_mutate])
        if char_to_mutate != "(" and char_to_mutate != ")":
            for boolean in true_and_false_list:
                pos_not_beginning_or_end = pos_to_mutate > 0 if boolean else pos_to_mutate + 1 < len(self)
                if pos_not_beginning_or_end:
                    symbol_to_check = self[pos_to_mutate + (-1 if boolean else 1)]
                for symbol in Symbol.symbols():
                    append = False
                    if pos_not_beginning_or_end:
                        if getattr(symbol_to_check, "forbidden_" + ("next" if boolean else "prev") + "_symbol")(symbol):
                            append = True
                    elif not symbol.starting_symbol if boolean else not symbol.ending_symbol:
                        append = True
                    if append and symbol not in forbidden_symbols:
                        forbidden_symbols.append(symbol)
        symbols_available_to_mutate_to = []
        for symbol in Symbol.symbols():
            if symbol != self[pos_to_mutate] and (
                    symbol not in forbidden_symbols or str(symbol) == "(" or str(symbol) == ")"):
                symbols_available_to_mutate_to.append(symbol)
        char_to_mutate = str(self[pos_to_mutate])
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

    def __clean_symbol_to_mutate_to(self, pos_to_mutate: int, symbol_to_mutate_to: Symbol):
        prefix = None
        suffix = None
        symbol_to_mutate = self[pos_to_mutate]
        prev_symbol = self[pos_to_mutate - 1] if pos_to_mutate > 0 else None
        next_symbol = self[pos_to_mutate + 1] if pos_to_mutate + 1 < len(self) else None

        if isinstance(symbol_to_mutate, SingleArgFunction):
            if isinstance(symbol_to_mutate_to, Operator):
                id_len = len(self)
                # In case the length of the actual id is lesser than the wanted length,
                # we insert a variable prev to the negation to convert it to a subtraction.
                if id_len < wanted_length:
                    prefix = Number.random()
                # In case the length of the actual id is bigger than the wanted length, we remove the char to remove
                # the negation. In negative case, we flip a coin to decide if we remove the negation or add a variable.
                elif id_len > wanted_length or random_bool():
                    symbol_to_mutate_to = None
                else:
                    prefix = Number.random()
        elif str(symbol_to_mutate) == "(":
            suffix_or_prefix = isinstance(symbol_to_mutate_to, Number)
            num_or_function = isinstance(symbol_to_mutate_to, Function)
            not_able_to_remove_char = str(next_symbol) == "-" and pos_to_mutate > 0 and (
                        str(prev_symbol) == "-" or str(prev_symbol) == "+")
            # not_able_to_remove_char = next_char == '-' and self.pos_to_mutate > 0 and (prev_char == '+' or prev_char == '-')
            if isinstance(symbol_to_mutate_to, Number) or (
                    isinstance(symbol_to_mutate_to, Function) and (pos_to_mutate > 0 or str(next_symbol) == "-")):
            # if (char_to_mutate_to in numbers and next_char != '-') or (
            #         char_to_mutate_to in Operator.operators() and (self.pos_to_mutate > 0 or next_char == '-')):
                len_id = len(self.__symbols)
                # FIRST CONDITIONAL: This means id length will be 1 or more positions smaller than the wanted length
                # (because an ')' char will be later removed from the id).
                # SECOND CONDITIONAL: This means the id length will be equal to the wanted length after we remove an
                # ')' char. In negative case, we flip a coin to decide if we add a char to the chars_to_mutate_to
                # string or we don't insert any char at all.
                if len_id <= wanted_length or (len_id == wanted_length + 1 and random_bool()):
                    # Given we want the id length to be equal to the wanted length,
                    # we add a char either to the prefix or suffix
                    prefix, suffix = Id.__set_var_or_operator_to_suff_or_pref(num_or_function, suffix_or_prefix)
                # The only cases left to consider are the ones where the id length is 2 or more chars bigger than
                # the wanted length. In that case, for sure we don't insert any char at all.
                # If we don't insert any char at all, on ids where the char to mutate is surrounded by an '+'
                # and an '-' char, not inserting any char would transform the id from this: (let p be the rest
                # of chars of the id) 'ppp+(-ppp' to this 'ppp+-ppp'. On that case, we would set the char to
                # mutate to a number or a variable.
                else:
                    symbol_to_mutate_to = Number.random() if not_able_to_remove_char else None
            # In case char to mutate is an close parenthesis...
        elif str(symbol_to_mutate) == ')':
            suffix_or_prefix = isinstance(symbol_to_mutate_to, Function)
            num_or_function = isinstance(symbol_to_mutate_to, Function)
            if isinstance(symbol_to_mutate_to, Number) or (
                    isinstance(symbol_to_mutate_to, Operator) and not isinstance(next_symbol, SingleArgFunction)):
            # if char_to_mutate_to in numbers or (char_to_mutate_to in Operator.operators() and next_char != '-'):
                len_id = len(self)
                if len_id <= wanted_length or (len_id == wanted_length + 1 and random_bool()):
                    prefix, suffix = Id.__set_var_or_operator_to_suff_or_pref(num_or_function, suffix_or_prefix)
                else:
                    symbol_to_mutate_to = None

        if str(symbol_to_mutate_to) == '(':
            if isinstance(symbol_to_mutate, Number) and isinstance(next_symbol, Operator):
                suffix = Number.random()
            elif isinstance(symbol_to_mutate, Operator) and (
                    str(prev_symbol) == ")" or (prev_symbol and isinstance(prev_symbol, Number))):
                prefix = Operator.random()
            # if self.char_to_mutate in numbers and next_char in Operator.operators().replace("-", ""):
            #     suffix = random_number()
            # elif self.char_to_mutate in Operator.operators() and (
            #             prev_char == ')' or (prev_char != "" and prev_char in numbers)):
            #     prefix = Operator.random_operator()
        elif str(symbol_to_mutate_to) == ')':
            if isinstance(prev_symbol, Operator):
                prefix = Number.random()
                if next_symbol and (isinstance(next_symbol, Number) or str(next_symbol) == "("):
                    suffix = Operator.random()
            elif next_symbol and ((isinstance(prev_symbol, Number) and str(next_symbol) != "-") or (
                    str(prev_symbol) == ")" and str(next_symbol) != "-")):
                suffix = Operator.random()
            # if prev_char in Operator.operators():
            #     prefix = random_number()
            #     if next_char != '' and (next_char in numbers or next_char == '('):
            #         suffix = Operator.random_operator()
            # elif next_char != '' and ((prev_char in numbers and next_char != '-') or (
            #         prev_char == ')' and next_char != '-')):
            #     suffix = Operator.random_operator()

        final_symbols = []
        if prefix:
            final_symbols.append(prefix)
        if symbol_to_mutate_to:
            final_symbols.append(symbol_to_mutate_to)
        if suffix:
            final_symbols.append(suffix)

        return final_symbols

    # -- PUBLIC METHODS -- #

    @staticmethod
    def random(length=wanted_length):
        new_id = [Symbol.random_starting_symbol([OpenParenthesis()] if length < 6 else [])]
        last_close_parenthesis_pos = 0
        parenthesis_counter = 1 if str(new_id[-1]) == "(" else 0
        while len(new_id) < length or new_id[-1] not in Symbol.ending_symbols() or parenthesis_counter > 0:
            num_of_symbols_left_to_add = length - len(new_id)
            if parenthesis_counter > 0 and parenthesis_counter >= num_of_symbols_left_to_add:
                new_symbol = Id.__random_symbol_to_append_in_list_if_not_return_random([CloseParenthesis()], new_id[-1],
                                                                                       [OpenParenthesis()])
            else:
                exceptions = []
                if parenthesis_counter == 0 or len(new_id) - last_close_parenthesis_pos < 3:
                    exceptions.append(CloseParenthesis())
                if num_of_symbols_left_to_add <= 4 + parenthesis_counter:
                    exceptions.append(OpenParenthesis())
                if len(new_id) + 1 >= length:
                    new_symbol = Id.__random_symbol_to_append_in_list_if_not_return_random(Symbol.ending_symbols(),
                                                                                           new_id[-1], exceptions)
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
            pos_to_mutate = random.randint(0, len(self) - 1)
            symbols_available_to_mutate_to = self.__get_symbols_available_to_mutate_to(pos_to_mutate)
        symbol_to_mutate_to = random.choice(symbols_available_to_mutate_to)
        final_symbols = self.__clean_symbol_to_mutate_to(pos_to_mutate, symbol_to_mutate_to)
        symbol_list = self.__symbols[:pos_to_mutate] + final_symbols + self.__symbols[pos_to_mutate + 1:]
        new_id = Id(symbol_list)
        new_id = Id.__add_parenthesis_if_needed(new_id)
        return Id(new_id)

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


if __name__ == "__main__":
    id = Id.random(10)
    print(str(id))
    for i in range(100):
        print(str(id.mutate()))
