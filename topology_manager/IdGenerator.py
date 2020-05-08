from misc.Random import *


class IdGenerator:

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    @staticmethod
    def __valid_close_parenthesis(id, parenthesis_counter):
        if parenthesis_counter > 0:
            length_check = 0
            valid = True
            while length_check < 3 and valid:
                if len(id) > length_check and id[-(length_check+1)] == '(':
                    valid = False
                length_check += 1
            if valid:
                return True
        return False

    @staticmethod
    def __valid_open_parenthesis(id, parenthesis_counter, length):
        remain_to_fill = length - len(id)
        remain_to_fill = 0 if remain_to_fill < 0 else remain_to_fill
        return parenthesis_counter < remain_to_fill - 3

    # -------------------- #
    # -- PUBLIC METHODS -- #
    # -------------------- #

    @staticmethod
    def generate_id(length):
        new_id, is_open_parenthesis, is_close_parenthesis = random_char()
        parenthesis_counter = 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
        while new_id in plus_minus_array:
            new_id, is_open_parenthesis, is_close_parenthesis = random_char()
            parenthesis_counter = 1 if is_open_parenthesis else 0
        while len(new_id) < length or new_id[-1] in operators_array_left:
            new_c, is_open_parenthesis, is_close_parenthesis = random_char()
            while new_id[-1] in forbidden_left_chars[new_c] or (
                    is_close_parenthesis and not IdGenerator.__valid_close_parenthesis(new_id,
                                                                                       parenthesis_counter)) or (
                    is_open_parenthesis and not IdGenerator.__valid_open_parenthesis(new_id, parenthesis_counter,
                                                                                     length)):
                new_c, is_open_parenthesis, is_close_parenthesis = random_char()
            parenthesis_counter += 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
            new_id += new_c
        while parenthesis_counter > 0:
            if new_id[-1] in forbidden_left_chars[")"]:
                new_c, is_open_parenthesis, is_close_parenthesis = random_char()
                while new_id[-1] in forbidden_left_chars[new_c] or new_c == "(":
                    new_c, is_open_parenthesis, is_close_parenthesis = random_char()
                new_id += new_c
            else:
                new_id += ")"
                parenthesis_counter -= 1
        return new_id
