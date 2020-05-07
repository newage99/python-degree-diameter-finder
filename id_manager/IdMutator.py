from Random import *
import unittest


class IdMutator(unittest.TestCase):

    id = ""
    wanted_length = 0
    pos_to_mutate = -1
    char_to_mutate = ''

    # ---------------------------- #
    # -- PRIVATE STATIC METHODS -- #
    # ---------------------------- #

    @staticmethod
    def __is_negation(id, pos):
        return id[pos] == '-' and (pos == 0 or id[pos - 1] in operators or id[pos - 1] == '(')

    # Inserts a variable/number or an operator to the left or right of the value depending on the provided parameters
    @staticmethod
    def __set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix):
        char_to_set = random_var_or_number() if var_or_operator else random_operator()
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

    def __insert_open_parenthesis_until_pos(self, pos):
        positions_to_insert_open_parenthesis = []
        while pos >= 0:
            prev_char = self.id[pos - 1] if pos > 0 else ''
            if self.id[pos] == ')':
                pos -= 3
            elif (prev_char in (operators + "(") or prev_char == '') and self.id[pos] in (variables_and_numbers + "("):
                positions_to_insert_open_parenthesis.append(pos)
            pos -= 1
        there_are_positions_to_insert_open_parenthesis = len(positions_to_insert_open_parenthesis) > 0
        if there_are_positions_to_insert_open_parenthesis:
            pos = positions_to_insert_open_parenthesis[random.randint(0, len(positions_to_insert_open_parenthesis) - 1)]
            self.id = self.id[:pos] + "(" + self.id[pos:]
        return there_are_positions_to_insert_open_parenthesis

    def __insert_close_parenthesis_from_pos(self, pos):
        positions_to_insert_close_parenthesis = []
        len_id = len(self.id)
        while pos < len_id:
            prev_char = self.id[pos - 1] if pos > 0 else ''
            if self.id[pos] == '(':
                pos += 3
            elif prev_char in (variables_and_numbers + ")") and self.id[pos] in (operators + ")"):
                positions_to_insert_close_parenthesis.append(pos)
            pos += 1
        positions_to_insert_close_parenthesis.append(len_id)
        pos = positions_to_insert_close_parenthesis[random.randint(0, len(positions_to_insert_close_parenthesis) - 1)]
        if pos == len_id:
            self.id += ")"
        else:
            self.id = self.id[:pos] + ")" + self.id[pos:]

    def __add_parenthesis_if_needed(self):
        parenthesis_inserted = True
        while parenthesis_inserted:
            parenthesis_inserted = False
            parenthesis_counter = 0
            for i in range(len(self.id)):
                char = self.id[i]
                if char == '(':
                    parenthesis_counter += 1
                elif char == ')':
                    if parenthesis_counter == 0:
                        self.__insert_open_parenthesis_until_pos(i - 3)
                        parenthesis_inserted = True
                        break
                    parenthesis_counter -= 1
            # This means there has been one or more open parenthesis not closed.
            if not parenthesis_inserted and parenthesis_counter > 0:
                self.__insert_close_parenthesis_from_pos(self.id.rfind('(') + 4)
                parenthesis_inserted = True

    def __mutate_id(self):
        self.calculate_pos_to_mutate()
        chars_available_to_mutate_to = self.get_chars_available_to_mutate_to()
        char_to_mutate_to = chars_available_to_mutate_to[random.randint(0, len(chars_available_to_mutate_to) - 1)]
        prefix, char_to_mutate_to, suffix = self.clean_char_to_mutate_to(char_to_mutate_to)
        self.id = self.id[:self.pos_to_mutate] + prefix + char_to_mutate_to + suffix + self.id[self.pos_to_mutate + 1:]
        self.__add_parenthesis_if_needed()
        return self.id, self.pos_to_mutate, self.char_to_mutate, char_to_mutate_to

    # -------------------- #
    # -- PUBLIC METHODS -- #
    # -------------------- #

    def get_chars_available_to_mutate_to(self):

        chars_available_to_mutate_to = characters
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
                chars_available_to_mutate_to = chars_available_to_mutate_to.replace(operators, "") + "-"
        # If char to mutate is ')' or if we are to close to the end of the id or to a ')' char,
        # is not worth to mutate to char ')'.
        if char_to_mutate == ')' or self.__is_not_worth_mutate_to_open_parenthesis():
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("(", "")
        if char_to_mutate in variables_and_numbers:
            # In case we are going to mutate a variable or a number, we might mutate TO a variable, a number or
            # a parenthesis.
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace(operators, "")
        elif char_to_mutate in operators:
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
            if char_to_mutate_to in operators:
                id_len = len(self.id)
                # In case the length of the actual id is lesser than the wanted length,
                # we insert a variable prev to the negation to convert it to a subtraction.
                if id_len < self.wanted_length:
                    prefix = random_var_or_number()
                # In case the length of the actual id is bigger than the wanted length, we remove the char to remove
                # the negation. In negative case, we flip a coin to decide if we remove the negation or add a variable.
                elif id_len > self.wanted_length or random_bool():
                    char_to_mutate_to = ''
                else:
                    prefix = random_var_or_number()
        # In case char to mutate is an open parenthesis...
        elif self.char_to_mutate == '(':
            suffix_or_prefix = char_to_mutate_to in variables_and_numbers
            var_or_operator = char_to_mutate_to in operators
            not_able_to_remove_char = next_char == '-' and self.pos_to_mutate > 0 and prev_char == '+'
            if (char_to_mutate_to in variables_and_numbers and next_char != '-') or (
                    char_to_mutate_to in operators and (self.pos_to_mutate > 0 or next_char == '-')):
                len_id = len(self.id)
                # FIRST CONDITIONAL: This means id length will be 1 or more positions smaller than the wanted length
                # (because an ')' char will be later removed from the id).
                # SECOND CONDITIONAL: This means the id length will be equal to the wanted length after we remove an
                # ')' char. In negative case, we flip a coin to decide if we add a char to the chars_to_mutate_to
                # string or we don't insert any char at all.
                if len_id <= self.wanted_length or (len_id == self.wanted_length+1 and random_bool()):
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
            suffix_or_prefix = char_to_mutate_to in operators
            var_or_operator = char_to_mutate_to in operators
            if char_to_mutate_to in variables_and_numbers or (char_to_mutate_to in operators and next_char != '-'):
                len_id = len(self.id)
                if len_id <= self.wanted_length or (len_id == self.wanted_length+1 and random_bool()):
                    prefix, suffix = IdMutator.__set_var_or_operator_to_suff_or_pref(var_or_operator, suffix_or_prefix)
                else:
                    char_to_mutate_to = ''

        if char_to_mutate_to == '(':
            if self.char_to_mutate in variables_and_numbers and next_char in operators.replace("-", ""):
                suffix = random_var_or_number()
            elif self.char_to_mutate in operators and (prev_char == ')' or prev_char in variables_and_numbers):
                prefix = random_operator()
        elif char_to_mutate_to == ')':
            if prev_char in operators:
                prefix = random_var_or_number()
                if next_char != '' and (next_char in variables_and_numbers or next_char == '('):
                    suffix = random_operator()
            elif next_char != '' and ((prev_char in variables_and_numbers and next_char != '-') or (
                    prev_char == ')' and next_char != '-')):
                suffix = random_operator()

        return prefix, char_to_mutate_to, suffix

    def set_id_and_wanted_length(self, id_to_mutate, wanted_length):
        self.id = id_to_mutate
        self.wanted_length = wanted_length

    def calculate_pos_to_mutate(self):
        self.pos_to_mutate = random.randint(0, len(self.id) - 1)
        self.char_to_mutate = self.id[self.pos_to_mutate]

    def mutate_id(self, id_to_mutate, wanted_length=None):
        wanted_length = wanted_length if wanted_length else len(id_to_mutate)
        self.set_id_and_wanted_length(id_to_mutate, wanted_length)
        return self.__mutate_id()