from main.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator
from misc.config import wanted_length
from misc.Random import *
from symbols.Number import Number
from symbols.Operator import Operator
from symbols.Symbol import Symbol
from symbols.Variable import Variable


variables_and_numbers = Number.numbers() + Variable.variables()


def random_var_or_number():
    return random.choice(Number.numbers() + Variable.variables())


class IdMutator:

    def __init__(self):
        self.id = ""
        self.pos_to_mutate = -1
        self.char_to_mutate = ''

    # ---------------------------- #
    # -- PRIVATE STATIC METHODS -- #
    # ---------------------------- #

    @staticmethod
    def __is_negation(id, pos):
        return id[pos] == '-' and (pos == 0 or id[pos - 1] in Operator.operators() or id[pos - 1] == '(')

    # Inserts a variable/number or an operator to the left or right of the value depending on the provided parameters
    @staticmethod
    def __set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix):
        char_to_set = random_var_or_number() if var_or_operator else Operator.choice()
        return ('', char_to_set) if suffix_or_prefix else (char_to_set, '')

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    def __is_not_worth_mutate_to_open_parenthesis(self):

        len_id = len(self.id)
        pos_to_mutate_plus_four = self.pos_to_mutate + 4

        if pos_to_mutate_plus_four >= len_id:
            return True
        else:
            pos = self.pos_to_mutate + 1
            while pos < pos_to_mutate_plus_four:
                if self.id[pos] == ')':
                    return True
                pos += 1
        return False

    def __is_not_worth_mutate_to_close_parenthesis(self):

        if self.pos_to_mutate < 4:
            return True
        else:
            pos_to_mutate_minus_four = self.pos_to_mutate - 4
            pos = self.pos_to_mutate - 1
            while pos > pos_to_mutate_minus_four:
                if self.id[pos] == '(':
                    return True
                pos -= 1
        return False

    @staticmethod
    def insert_open_parenthesis_until_pos(id, pos):
        positions_to_insert_open_parenthesis = []
        while pos >= 0:
            prev_char = id[pos - 1] if pos > 0 else ''
            if id[pos] == ')':
                pos -= 3
            elif (prev_char in (Operator.operators() + "(") or prev_char == '') and id[pos] in (variables_and_numbers + "("):
                positions_to_insert_open_parenthesis.append(pos)
            pos -= 1
        there_are_positions_to_insert_open_parenthesis = len(positions_to_insert_open_parenthesis) > 0
        if there_are_positions_to_insert_open_parenthesis:
            pos = positions_to_insert_open_parenthesis[random.randint(0, len(positions_to_insert_open_parenthesis) - 1)]
            return id[:pos] + "(" + id[pos:]
        return id

    @staticmethod
    def insert_close_parenthesis_from_pos(id, pos):
        positions_to_insert_close_parenthesis = []
        len_id = len(id)
        while pos < len_id:
            prev_char = id[pos - 1] if pos > 0 else ''
            if id[pos] == '(':
                pos += 3
            elif prev_char in (variables_and_numbers + ")") and id[pos] in (Operator.operators() + ")"):
                positions_to_insert_close_parenthesis.append(pos)
            pos += 1
        positions_to_insert_close_parenthesis.append(len_id)
        pos = positions_to_insert_close_parenthesis[random.randint(0, len(positions_to_insert_close_parenthesis) - 1)]
        if pos == len_id:
            return id + ")"
        return id[:pos] + ")" + id[pos:]

    @staticmethod
    def add_parenthesis_if_needed(id):
        parenthesis_inserted = True
        while parenthesis_inserted:
            parenthesis_inserted = False
            parenthesis_counter = 0
            for i in range(len(id)):
                char = id[i]
                if char == '(':
                    parenthesis_counter += 1
                elif char == ')':
                    if parenthesis_counter == 0:
                        id = IdMutator.insert_open_parenthesis_until_pos(id, i - 3)
                        parenthesis_inserted = True
                        break
                    parenthesis_counter -= 1
            # This means there has been one or more open parenthesis not closed.
            if not parenthesis_inserted and parenthesis_counter > 0:
                id = IdMutator.insert_close_parenthesis_from_pos(id, id.rfind('(') + 4)
                parenthesis_inserted = True
        return id

    def __mutate_id(self, get_additional_data: bool):
        self.calculate_pos_to_mutate()
        chars_available_to_mutate_to = self.get_chars_available_to_mutate_to()
        char_to_mutate_to = chars_available_to_mutate_to[random.randint(0, len(chars_available_to_mutate_to) - 1)]
        prefix, char_to_mutate_to, suffix = self.clean_char_to_mutate_to(char_to_mutate_to)
        new_id = self.id[:self.pos_to_mutate] + prefix + char_to_mutate_to + suffix + self.id[self.pos_to_mutate + 1:]
        new_id = IdMutator.add_parenthesis_if_needed(new_id)
        if get_additional_data:
            return new_id, self.pos_to_mutate, self.char_to_mutate, char_to_mutate_to, prefix, suffix
        return new_id

    # -------------------- #
    # -- PUBLIC METHODS -- #
    # -------------------- #

    def get_chars_available_to_mutate_to(self):
        chars_available_to_mutate_to = ''.join(list(Symbol.symbols_dict().keys()))
        char_to_mutate = self.id[self.pos_to_mutate]
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(char_to_mutate, "")

        if char_to_mutate == '(' or self.__is_not_worth_mutate_to_close_parenthesis():
            # If char to mutate is '(' or if we are to close to the beginning of the id or to a '(' char,
            # is not worth to mutate to char ')'.
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace(")", "")
            # If char to mutate is '('...
            if char_to_mutate == '(' and self.pos_to_mutate == 0:
                # and it's located at the beginning of the id, placing an operator (except
                # '-' one) there makes no sense. Examples: (n+1) -> /n+1), (n+1) -> *n+1)
                chars_available_to_mutate_to = chars_available_to_mutate_to.replace(Operator.operators(), "") + "-"
        # If char to mutate is ')' or if we are to close to the end of the id or to a ')' char,
        # is not worth to mutate to char ')'.
        if char_to_mutate == ')' or self.__is_not_worth_mutate_to_open_parenthesis():
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("(", "")
        if char_to_mutate in variables_and_numbers:
            # In case we are going to mutate a variable or a number, we might mutate TO a variable, a number or
            # a parenthesis.
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace(Operator.operators(), "")
        elif char_to_mutate in Operator.operators():
            # In case we are going to mutate an operator, we might mutate TO an operator or a parenthesis.
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace(variables_and_numbers, "")

        # If next char is '-', means that replacing to '+' or '-' would create a wrong expressions '+-' and '--'.
        if self.pos_to_mutate + 1 < len(self.id) and self.id[self.pos_to_mutate + 1] == '-':
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("+", "")
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("-", "")

        return chars_available_to_mutate_to

    def clean_char_to_mutate_to(self, char_to_mutate_to):
        prefix = ''
        suffix = ''
        prev_char = self.id[self.pos_to_mutate - 1] if self.pos_to_mutate > 0 else ''
        next_char = self.id[self.pos_to_mutate + 1] if self.pos_to_mutate + 1 < len(self.id) else ''
        char_to_mutate_is_negation = IdMutator.__is_negation(self.id, self.pos_to_mutate)

        # In case char to mutate is a negation...
        if char_to_mutate_is_negation:
            if char_to_mutate_to in Operator.operators():
                id_len = len(self.id)
                # In case the length of the actual id is lesser than the wanted length,
                # we insert a variable prev to the negation to convert it to a subtraction.
                if id_len < wanted_length:
                    prefix = random_var_or_number()
                # In case the length of the actual id is bigger than the wanted length, we remove the char to remove
                # the negation. In negative case, we flip a coin to decide if we remove the negation or add a variable.
                elif id_len > wanted_length or random_bool():
                    char_to_mutate_to = ''
                else:
                    prefix = random_var_or_number()
        # In case char to mutate is an open parenthesis...
        elif self.char_to_mutate == '(':
            suffix_or_prefix = char_to_mutate_to in variables_and_numbers
            var_or_operator = char_to_mutate_to in Operator.operators()
            not_able_to_remove_char = next_char == '-' and self.pos_to_mutate > 0 and (
                        prev_char == '+' or prev_char == '-')
            if (char_to_mutate_to in variables_and_numbers and next_char != '-') or (
                    char_to_mutate_to in Operator.operators() and (self.pos_to_mutate > 0 or next_char == '-')):
                len_id = len(self.id)
                # FIRST CONDITIONAL: This means id length will be 1 or more positions smaller than the wanted length
                # (because an ')' char will be later removed from the id).
                # SECOND CONDITIONAL: This means the id length will be equal to the wanted length after we remove an
                # ')' char. In negative case, we flip a coin to decide if we add a char to the chars_to_mutate_to
                # string or we don't insert any char at all.
                if len_id <= wanted_length or (len_id == wanted_length+1 and random_bool()):
                    # Given we want the id length to be equal to the wanted length,
                    # we add a char either to the prefix or suffix
                    prefix, suffix = IdMutator.__set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix)
                # The only cases left to consider are the ones where the id length is 2 or more chars bigger than
                # the wanted length. In that case, for sure we don't insert any char at all.
                # If we don't insert any char at all, on ids where the char to mutate is surrounded by an '+'
                # and an '-' char, not inserting any char would transform the id from this: (let p be the rest
                # of chars of the id) 'ppp+(-ppp' to this 'ppp+-ppp'. On that case, we would set the char to
                # mutate to a number or a variable.
                else:
                    char_to_mutate_to = random_var_or_number() if not_able_to_remove_char else ''
        # In case char to mutate is an close parenthesis...
        elif self.char_to_mutate == ')':
            suffix_or_prefix = char_to_mutate_to in Operator.operators()
            var_or_operator = char_to_mutate_to in Operator.operators()
            if char_to_mutate_to in variables_and_numbers or (char_to_mutate_to in Operator.operators() and next_char != '-'):
                len_id = len(self.id)
                if len_id <= wanted_length or (len_id == wanted_length+1 and random_bool()):
                    prefix, suffix = IdMutator.__set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix)
                else:
                    char_to_mutate_to = ''

        if char_to_mutate_to == '(':
            if self.char_to_mutate in variables_and_numbers and next_char in Operator.operators().replace("-", ""):
                suffix = random_var_or_number()
            elif self.char_to_mutate in Operator.operators() and (prev_char == ')' or prev_char in variables_and_numbers):
                prefix = Operator.choice()
        elif char_to_mutate_to == ')':
            if prev_char in Operator.operators():
                prefix = random_var_or_number()
                if next_char != '' and (next_char in variables_and_numbers or next_char == '('):
                    suffix = Operator.choice()
            elif next_char != '' and ((prev_char in variables_and_numbers and next_char != '-') or (
                    prev_char == ')' and next_char != '-')):
                suffix = Operator.choice()

        return prefix, char_to_mutate_to, suffix

    def calculate_pos_to_mutate(self):
        self.pos_to_mutate = random.randint(0, len(self.id) - 1)
        self.char_to_mutate = self.id[self.pos_to_mutate]

    # --------------------------- #
    # -- PUBLIC STATIC METHODS -- #
    # --------------------------- #

    @staticmethod
    def mutate_id(id_to_mutate, get_additional_data: bool = False):
        id_mutator = IdMutator()
        id_mutator.id = id_to_mutate
        return id_mutator.__mutate_id(get_additional_data)

    @staticmethod
    def mutate_to_connected_matrix_id(id_to_mutate, prohibited_ids=None):
        if prohibited_ids is None:
            prohibited_ids = []
        connected = False
        while not connected:
            prohibited_id = True
            while prohibited_id:
                mutated_id = IdMutator.mutate_id(id_to_mutate)
                prohibited_id = mutated_id in prohibited_ids
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(mutated_id)
        return mutated_id, matrix
