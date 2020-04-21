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
characters = "+-*/%^L()xyn12"
