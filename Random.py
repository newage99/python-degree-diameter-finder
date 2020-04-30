import random
from global_variables import *


def random_bool() -> bool:
    return bool(random.getrandbits(1))


def random_char():
    new_c = characters[random.randint(0, len(characters) - 1)]
    return new_c, new_c == '(', new_c == ')'


def random_var_or_number():
    return variables_and_numbers[random.randint(0, len(variables_and_numbers) - 1)]


def random_operator():
    return operators[random.randint(0, len(operators) - 1)]