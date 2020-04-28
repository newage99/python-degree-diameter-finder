import random
from global_variables import *


id = ""
n = 0


def random_bool() -> bool:
    return bool(random.getrandbits(1))


def valid_close_parenthesis(id, parenthesis_counter):
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


def valid_open_parenthesis(id, parenthesis_counter, length):
    remain_to_fill = length - len(id)
    remain_to_fill = 0 if remain_to_fill < 0 else remain_to_fill
    return parenthesis_counter < remain_to_fill - 3


def random_char():
    new_c = characters[random.randint(0, len(characters) - 1)]
    return new_c, new_c == '(', new_c == ')'


# TODO: Analize and decide if it's worth to refactor this function.
def random_id(length):
    new_id, is_open_parenthesis, is_close_parenthesis = random_char()
    parenthesis_counter = 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
    while new_id in plus_minus_array:
        new_id, is_open_parenthesis, is_close_parenthesis = random_char()
        parenthesis_counter = 1 if is_open_parenthesis else 0
    while len(new_id) < length or new_id[-1] in operators_array_left:
        new_c, is_open_parenthesis, is_close_parenthesis = random_char()
        while new_id[-1] in forbidden_left_chars[new_c] or \
                (is_close_parenthesis and not valid_close_parenthesis(new_id, parenthesis_counter)) or \
                (is_open_parenthesis and not valid_open_parenthesis(new_id, parenthesis_counter, length)):
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


def is_not_worth_mutate_to_open_parenthesis(pos_to_mutate):

    if pos_to_mutate < 4:
        return True
    else:
        # TODO: Check there's no open parenthesis on the 4 chars prev to the one to mutate
        pass

    return False


# TODO
def is_not_worth_mutate_to_close_parenthesis(pos_to_mutate):
    pass


# TODO: Implement test to this function.
def get_chars_available_to_mutate_to(id, pos_to_mutate):

    operators = "+-*/%^L"
    variables_and_numbers = "xyn12"
    chars_available_to_mutate_to = characters
    char_to_mutate = id[pos_to_mutate]
    chars_available_to_mutate_to = chars_available_to_mutate_to.replace(char_to_mutate, "")

    if char_to_mutate in variables_and_numbers:
        # In case we are going to mutate a variable or a number, we might mutate TO a variable or number.
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(operators, "")
    elif char_to_mutate in operators or char_to_mutate == ')':
        # In case we are going to mutate an operator, we might mutate TO an operator.
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(variables_and_numbers, "")
        # If the next char to the operator is '-', means that it's a negation, not a subtraction.
        if char_to_mutate != ')' and pos_to_mutate + 1 < len(id) and id[pos_to_mutate + 1] == '-':
            # In that case, we also restrict mutation to '-' and '+' operators, given they don't fit well with negation.
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("+", "")
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("-", "")
    # If char to mutate is '(' or if we are to close to the beginning of the id or to a '(' char,
    # is not worth to mutate to char ')'.
    elif char_to_mutate == '(' or is_not_worth_mutate_to_open_parenthesis(pos_to_mutate):
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(")", "")
    # If char to mutate is ')' or if we are to close to the end of the id or to a ')' char,
    # is not worth to mutate to char ')'.
    elif char_to_mutate == ')' or is_not_worth_mutate_to_close_parenthesis(pos_to_mutate):
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace("(", "")

    return chars_available_to_mutate_to


def get_chars_to_mutate_to(id, pos_to_mutate, chars_available_to_mutate_to):

    operators = "+-*/%^L"
    variables_and_numbers = "xyn12"
    char_to_mutate = id[pos_to_mutate]
    chars_to_mutate_to = chars_available_to_mutate_to[random.randint(0, len(chars_available_to_mutate_to) - 1)]
    prev_char = id[pos_to_mutate - 1]
    # In case char to mutate is a negation...
    if char_to_mutate == '-' and (pos_to_mutate == 0 or prev_char in operators or prev_char == '('):
        if chars_to_mutate_to in operators:
            id_len = len(id)
            if id_len < n:
                # In case the length of the actual id is lesser than the wanted length,
                # we insert a variable prev to the negation to convert it to a subtraction.
                chars_to_mutate_to = variables_and_numbers[random.randint(0, len(variables_and_numbers) - 1)]
            elif id_len > n:
                # In case the length of the actual id is bigger than the wanted length,
                # we remove the char to remove the negation.
                chars_to_mutate_to = ''
            else:
                # Otherwise, we flip a coin to decide if we add a variable or remove the negation.
                chars_to_mutate_to = '' if random_bool() else variables_and_numbers[
                    random.randint(0, len(variables_and_numbers) - 1)]
    elif char_to_mutate == '(':
        pass  # TODO
    elif char_to_mutate == ')':
        pass  # TODO
    return chars_to_mutate_to


def mutate_id_inner():

    pos_to_mutate = random.randint(0, len(id) - 1)
    variables_and_numbers = "xyn12"
    chars_available_to_mutate_to = get_chars_available_to_mutate_to(id, pos_to_mutate)
    chars_to_mutate_to = get_chars_to_mutate_to(id, pos_to_mutate, chars_available_to_mutate_to)

    new_id = id[:pos_to_mutate] + chars_to_mutate_to + id[pos_to_mutate + 1:]

    # TODO: Remove code below and only implement inserting of open or close parenthesis if it's needed.

    if char_to_mutate == '(':
        close_parenthesis_positions = []
        pos = pos_to_mutate + 3
        while pos < len(new_id):
            if new_id[pos] == ')':
                close_parenthesis_positions.append(pos)
            pos += 1
        pos_to_remove_close = close_parenthesis_positions[random.randint(0, len(close_parenthesis_positions) - 1)]
        new_id = new_id[:pos_to_remove_close] + new_id[pos_to_remove_close + 1:]
    elif char_to_mutate == ')':
        if pos_to_mutate + 1 == len(new_id) and char_to_mutate_to in operators:
            new_id += variables_and_numbers[random.randint(0, len(variables_and_numbers) - 1)]
        open_parenthesis_positions = []
        pos = pos_to_mutate - 3
        while pos >= 0:
            if new_id[pos] == '(':
                open_parenthesis_positions.append(pos)
            pos -= 1
        pos_to_remove_open = open_parenthesis_positions[random.randint(0, len(open_parenthesis_positions) - 1)]
        new_id = new_id[:pos_to_remove_open] + new_id[pos_to_remove_open + 1:]

    if char_to_mutate_to == '(':
        pos_to_mutate_plus_one = pos_to_mutate + 1
        if new_id[pos_to_mutate_plus_one] in operators and new_id[pos_to_mutate_plus_one] != '-':
            new_id = new_id[:pos_to_mutate_plus_one] + new_id[pos_to_mutate_plus_one + 1:]
        pos_to_mutate_minus_one = pos_to_mutate - 1
        if pos_to_mutate_minus_one >= 0 and new_id[pos_to_mutate_minus_one] in variables_and_numbers:
            new_id = new_id[:pos_to_mutate] + operators[random.randint(0, len(operators) - 1)] + new_id[pos_to_mutate:]
        valid_positions_to_close = []
        pos = pos_to_mutate + 4
        while pos < len(new_id):
            if new_id[pos] in operators and (not (new_id[pos - 1] in operators)) and new_id[pos - 1] != '(':
                valid_positions_to_close.append(pos)
            pos += 1
        if len(valid_positions_to_close) <= 0:
            new_id += ")"
        else:
            pos_to_close = valid_positions_to_close[random.randint(0, len(valid_positions_to_close) - 1)]
            new_id = new_id[:pos_to_close] + ")" + new_id[pos_to_close:]
    elif char_to_mutate_to == ')':
        pos_to_mutate_plus_one = pos_to_mutate + 1
        if pos_to_mutate_plus_one < len(new_id) and (new_id[pos_to_mutate_plus_one] in variables_and_numbers or new_id[pos_to_mutate_plus_one] == '('):
            new_id = new_id[:pos_to_mutate_plus_one] + operators[random.randint(0, len(operators) - 1)] + new_id[pos_to_mutate_plus_one:]
        if char_to_mutate == '-' and new_id[pos_to_mutate - 1] in operators:
            new_id = new_id[:pos_to_mutate - 1] + new_id[pos_to_mutate:]
        valid_positions_to_insert_open = []
        pos = pos_to_mutate - 3
        while pos >= 0:
            if new_id[pos] in variables_and_numbers or new_id[pos] == '(':
                valid_positions_to_insert_open.append(pos)
            pos -= 1
        if len(valid_positions_to_insert_open) <= 0:
            new_id = '(' + new_id
        else:
            pos_to_insert_open = valid_positions_to_insert_open[random.randint(0, len(valid_positions_to_insert_open) - 1)]
            new_id = new_id[:pos_to_insert_open] + '(' + new_id[pos_to_insert_open:]

    if ")(" in new_id:
        pos = new_id.index(")(")
        new_id = new_id[:pos + 1] + operators[random.randint(0, len(operators) - 1)] + new_id[pos + 1:]

    new_id = new_id.replace("+-", "-")
    new_id = new_id.replace("--", "+")

    return new_id, pos_to_mutate, char_to_mutate, char_to_mutate_to


def mutate_id(id_to_mutate, wanted_length):

    n = wanted_length
    id = id_to_mutate
    mutate_id_inner()
