from misc.config import wanted_length
from symbols.interpretable_symbols.CloseParenthesis import CloseParenthesis
from symbols.interpretable_symbols.functions.operators.Operator import Operator
from symbols.Id import Id
from symbols.Symbol import Symbol


class IdGenerator:

    # --------------------- #
    # -- PRIVATE METHODS -- #
    # --------------------- #

    parenthesis_counter = 0

    @staticmethod
    def __valid_close_parenthesis(id):
        if IdGenerator.parenthesis_counter > 0:
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
    def __valid_open_parenthesis(id, length):
        remain_to_fill = length - len(id)
        remain_to_fill = 0 if remain_to_fill < 0 else remain_to_fill
        return IdGenerator.parenthesis_counter < remain_to_fill - 3

    # -------------------- #
    # -- PUBLIC METHODS -- #
    # -------------------- #

    @staticmethod
    def generate_id(length=wanted_length):
        operators = Operator.operators()
        new_id, is_open_parenthesis, is_close_parenthesis = Symbol.random_starting_symbol()
        new_id_symbols = [Symbol.parse(new_id)]
        IdGenerator.parenthesis_counter = 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
        while len(new_id) < length or new_id[-1] in operators or new_id[-1] == "(":
            new_c, is_open_parenthesis, is_close_parenthesis = Symbol.random()
            new_symbol = Symbol.parse(new_c, new_id_symbols[-1])
            while new_symbol is None or (
                    is_close_parenthesis and not IdGenerator.__valid_close_parenthesis(new_id)) or (
                    is_open_parenthesis and not IdGenerator.__valid_open_parenthesis(new_id, length)):
                new_c, is_open_parenthesis, is_close_parenthesis = Symbol.random()
                new_symbol = Symbol.parse(new_c, new_id_symbols[-1])
            IdGenerator.parenthesis_counter += 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
            new_id += new_c
            new_id_symbols.append(new_symbol)
        close_parenthesis_symbol = CloseParenthesis()
        while IdGenerator.parenthesis_counter > 0:
            if close_parenthesis_symbol.forbidden_prev_symbol(new_id_symbols[-1]):
                new_c, is_open_parenthesis, is_close_parenthesis = Symbol.random()
                new_symbol = Symbol.parse(new_c, new_id_symbols[-1])
                while new_symbol is None or new_c == "(":
                    new_c, is_open_parenthesis, is_close_parenthesis = Symbol.random()
                    new_symbol = Symbol.parse(new_c, new_id_symbols[-1])
                new_id += new_c
                new_id_symbols.append(new_symbol)
            else:
                new_id += ")"
                new_id_symbols.append(close_parenthesis_symbol)
                IdGenerator.parenthesis_counter -= 1
        return new_id

    @staticmethod
    def generate_connected_matrix_id():
        connected = False
        while not connected:
            # id = IdGenerator.generate_id()
            id = str(Id.random())
            from main.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(id)
        return id
