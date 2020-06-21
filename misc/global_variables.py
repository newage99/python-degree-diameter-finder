variables = ["x", "y", "n"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
variables_and_numbers = variables + numbers
vars_numbers_and_open_parenthesis = variables_and_numbers + ["("]
plus_minus_array = ["+", "-", "*", "/", "^", "L", "%", ")"]
operators_array = ["+", "*", "/", "%", ")", "^", "L"]
forbidden_right_chars = {
    "x": vars_numbers_and_open_parenthesis,
    "y": vars_numbers_and_open_parenthesis,
    "n": vars_numbers_and_open_parenthesis,
    "+": plus_minus_array,
    "-": plus_minus_array,
    "*": operators_array,
    "/": operators_array,
    "%": operators_array,
    "^": operators_array,
    "L": operators_array,
    "(": ["+", "*", "/", "%", ")", "^", "L"],
    ")": variables_and_numbers,
    "0": variables_and_numbers,
    "1": variables_and_numbers,
    "2": variables_and_numbers,
    "3": variables_and_numbers,
    "4": variables_and_numbers,
    "5": variables_and_numbers,
    "6": variables_and_numbers,
    "7": variables_and_numbers,
    "8": variables_and_numbers,
    "9": variables_and_numbers
}
vars_numbers_and_close_parenthesis = variables_and_numbers + [")"]
operators_array_left = ["+", "-", "*", "/", "%", "^", "L", "("]
sum_close_parenthesis_left = ["+", "-", "*", "/", "%", "^", "L", "("]
forbidden_left_chars = {
    "x": vars_numbers_and_close_parenthesis,
    "y": vars_numbers_and_close_parenthesis,
    "n": vars_numbers_and_close_parenthesis,
    "+": sum_close_parenthesis_left,
    "-": ["+", "-"],
    "*": operators_array_left,
    "/": operators_array_left,
    "%": operators_array_left,
    "^": operators_array_left,
    "L": operators_array_left,
    "(": vars_numbers_and_close_parenthesis,
    ")": sum_close_parenthesis_left,
    "0": vars_numbers_and_close_parenthesis,
    "1": vars_numbers_and_close_parenthesis,
    "2": vars_numbers_and_close_parenthesis,
    "3": vars_numbers_and_close_parenthesis,
    "4": vars_numbers_and_close_parenthesis,
    "5": vars_numbers_and_close_parenthesis,
    "6": vars_numbers_and_close_parenthesis,
    "7": vars_numbers_and_close_parenthesis,
    "8": vars_numbers_and_close_parenthesis,
    "9": vars_numbers_and_close_parenthesis
}
operators = "+-*/%^L"
characters = operators + "()xyn12"
variables_and_numbers = characters.replace(operators, "").replace("()", "")
