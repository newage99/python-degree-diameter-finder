import random

variables = ["x", "y", "n"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
numbers_array = variables + numbers
xyn_array = numbers_array + ["("]
plus_minus_array = ["+", "-", "*", "/", "^", "L", "%", ")"]
operators_array = ["+", "*", "/", "%", ")", "^", "L"]
forbidden_right_chars = {
    "x": xyn_array,
    "y": xyn_array,
    "n": xyn_array,
    "+": plus_minus_array,
    "-": plus_minus_array,
    "*": operators_array,
    "/": operators_array,
    "%": operators_array,
    "^": operators_array,
    "L": operators_array,
    "(": ["+", "*", "/", "%", ")", "^", "L"],
    ")": numbers_array,
    "0": numbers_array,
    "1": numbers_array,
    "2": numbers_array,
    "3": numbers_array,
    "4": numbers_array,
    "5": numbers_array,
    "6": numbers_array,
    "7": numbers_array,
    "8": numbers_array,
    "9": numbers_array
}
array_left = variables + [")"] + numbers
xyn_array_left = variables + [")"] + numbers
operators_array_left = ["+", "-", "*", "/", "%", "^", "L", "("]
sum_close_parenthesis_left = ["+", "-", "*", "/", "%", "^", "L", "("]
forbidden_left_chars = {
    "x": array_left,
    "y": array_left,
    "n": array_left,
    "+": sum_close_parenthesis_left,
    "-": ["+", "-"],
    "*": operators_array_left,
    "/": operators_array_left,
    "%": operators_array_left,
    "^": operators_array_left,
    "L": operators_array_left,
    "(": array_left,
    ")": sum_close_parenthesis_left,
    "0": array_left,
    "1": array_left,
    "2": array_left,
    "3": array_left,
    "4": array_left,
    "5": array_left,
    "6": array_left,
    "7": array_left,
    "8": array_left,
    "9": array_left
}
every = 0
characters = "+-*/%^L()xyn12"
beginning = ""
size = []
calculation_thread = None
calculation_on = True


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


def mutate_id(id):
    pos_to_mutate = random.randint(0, len(id) - 1)
    chars_available_to_mutate_to = "+-*/%^L()xyn12"
    if pos_to_mutate < 4 or (pos_to_mutate + 1 < len(id) and id[pos_to_mutate + 1] == '('):
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(")", "")
    if pos_to_mutate + 4 > len(id) or id[pos_to_mutate + 1] == ')':
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace("(", "")
    operators = "+-*/%^L"
    variables = "xyn12"
    char_to_mutate = id[pos_to_mutate]
    suffix = ''
    prefix = ''
    if char_to_mutate in operators:
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(variables, "")
        if pos_to_mutate + 1 < len(id) and id[pos_to_mutate + 1] == '-':
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("-", "")
            chars_available_to_mutate_to = chars_available_to_mutate_to.replace("+", "")
        if char_to_mutate == '-' and (pos_to_mutate == 0 or id[pos_to_mutate - 1] == '('):
            prefix = variables[random.randint(0, len(variables) - 1)]
    elif char_to_mutate in variables or char_to_mutate == '(':
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(operators, "")
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(")", "")
    if char_to_mutate == '(' and id[pos_to_mutate + 1] != '-':
        suffix = operators[random.randint(0, len(operators) - 1)]
    elif char_to_mutate == ')':
        chars_available_to_mutate_to = chars_available_to_mutate_to.replace(variables, "")
        suffix = variables[random.randint(0, len(variables) - 1)]

    chars_available_to_mutate_to = chars_available_to_mutate_to.replace(char_to_mutate, "")
    char_to_mutate_to = chars_available_to_mutate_to[random.randint(0, len(chars_available_to_mutate_to) - 1)]
    new_id = id[:pos_to_mutate] + prefix + char_to_mutate_to + suffix + id[pos_to_mutate + 1:]

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
            new_id += variables[random.randint(0, len(variables) - 1)]
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
        if pos_to_mutate_minus_one >= 0 and new_id[pos_to_mutate_minus_one] in variables:
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
        if pos_to_mutate_plus_one < len(new_id) and (new_id[pos_to_mutate_plus_one] in variables or new_id[pos_to_mutate_plus_one] == '('):
            new_id = new_id[:pos_to_mutate_plus_one] + operators[random.randint(0, len(operators) - 1)] + new_id[pos_to_mutate_plus_one:]
        if char_to_mutate == '-' and new_id[pos_to_mutate - 1] in operators:
            new_id = new_id[:pos_to_mutate - 1] + new_id[pos_to_mutate:]
        valid_positions_to_insert_open = []
        pos = pos_to_mutate - 3
        while pos >= 0:
            if new_id[pos] in variables or new_id[pos] == '(':
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
