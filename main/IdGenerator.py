from misc.config import wanted_length
from symbols.Operator import Operator
from symbols.Symbol import Symbol


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
    def generate_id(length=wanted_length):
        symbols_raw = Symbol.symbols_dict()
        symbols = {}
        for symbol in symbols_raw:
            symbols[symbol] = symbols_raw[symbol][0]
        new_id, is_open_parenthesis, is_close_parenthesis = Symbol.choice()
        new_id_symbols = [symbols[new_id]]
        parenthesis_counter = 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
        while new_id in Operator.operators() or new_id == ")":
            new_id, is_open_parenthesis, is_close_parenthesis = Symbol.choice()
            new_id_symbols = [symbols[new_id]]
            parenthesis_counter = 1 if is_open_parenthesis else 0
        while len(new_id) < length or new_id[-1] in Operator.operators() or new_id[-1] == "(":
            new_c, is_open_parenthesis, is_close_parenthesis = Symbol.choice()
            while symbols[new_c].forbidden_prev_symbol(new_id_symbols[-1]) or (
                    is_close_parenthesis and not IdGenerator.__valid_close_parenthesis(new_id,
                                                                                       parenthesis_counter)) or (
                    is_open_parenthesis and not IdGenerator.__valid_open_parenthesis(new_id, parenthesis_counter,
                                                                                     length)):
                new_c, is_open_parenthesis, is_close_parenthesis = Symbol.choice()
            parenthesis_counter += 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
            new_id += new_c
            new_id_symbols.append(symbols[new_c])
        close_parenthesis_symbol = symbols[")"]
        while parenthesis_counter > 0:
            if close_parenthesis_symbol.forbidden_prev_symbol(new_id_symbols[-1]):
                new_c, is_open_parenthesis, is_close_parenthesis = Symbol.choice()
                while symbols[new_c].forbidden_prev_symbol(new_id_symbols[-1]) or new_c == "(":
                    new_c, is_open_parenthesis, is_close_parenthesis = Symbol.choice()
                new_id += new_c
                new_id_symbols.append(symbols[new_c])
            else:
                new_id += ")"
                new_id_symbols.append(symbols[")"])
                parenthesis_counter -= 1
        return new_id

    @staticmethod
    def generate_connected_matrix_id():
        connected = False
        while not connected:
            id = IdGenerator.generate_id()
            from main.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(id)
        return id
