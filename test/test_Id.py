import unittest

from classes.interpretable_symbols.functions.operators.Operator import Operator
from classes.Symbol import Symbol
from classes.Id import Id


def print_error(self, pos_to_mutate, id, char_to_mutate, char_to_mutate_to, prefix, suffix, j, error):
    print('')
    if pos_to_mutate == -1:
        print(id)
    else:
        print(id + ' pos_to_mutate=' + str(pos_to_mutate) + ', char_to_mutate=' + char_to_mutate +
              ', char_to_mutate_to=' + char_to_mutate_to + ', prefix=' + prefix + ', suffix=' + suffix)
    print((' ' * j) + '^ char \'' + id[j] + '\' must not be ' + (
        'preceded' if error == 'L' else 'followed') + ' by char \'' + id[
              j + (-1 if error == 'L' else 1)] + '\'')
    self.assertTrue(False)  # We use this assert only to stop the test.


def check_id(self, id, pos_to_mutate: int = -1, char_to_mutate: str = '', char_to_mutate_to: str = '', prefix: str = '',
             suffix: str = '', check_parenthesis: bool = True):
    id_len = len(id)
    if type(id) is str:
        symbols = []
        prev_char = None
        for j in range(id_len):
            symbol = Symbol.parse(id[j], prev_number_or_symbol=prev_char)
            if symbol:
                symbols.append(symbol)
            else:
                print_error(self, pos_to_mutate, id, char_to_mutate, char_to_mutate_to, prefix, suffix, j, 'L')
            prev_char = symbol
    else:
        symbols = id
        id = str(symbols)
        for j in range(1, id_len):
            if not symbols[j].check_prev_symbol(symbols[j - 1]):
                print_error(self, pos_to_mutate, id, char_to_mutate, char_to_mutate_to, prefix, suffix, j, 'L')
    parenthesis_counter = 0
    for j in range(id_len):
        if id[j] == '(':
            parenthesis_counter += 1
        elif id[j] == ')':
            if check_parenthesis:
                self.assertTrue(parenthesis_counter >= 0,
                                "Found close parenthesis when there's no open parenthesis to close.")
            parenthesis_counter -= 1
        error = ''
        if j > 0 and symbols[j].forbidden_prev_symbol(symbols[j - 1]):
            error = 'L'
        elif j + 1 < id_len and symbols[j].forbidden_next_symbol(symbols[j + 1]):
            error = 'R'
        if error != '':
            print_error(self, pos_to_mutate, id, char_to_mutate, char_to_mutate_to, prefix, suffix, j, error)
    if check_parenthesis:
        self.assertEqual(parenthesis_counter, 0, "Incorrect number of parenthesis.")
    try:
        self.assertFalse(id[id_len - 1] in Operator.operators(), "Id ends with an invalid character.")
    except Exception as e:
        a = 0


class IdTest(unittest.TestCase):

    def test_random(self):
        ids_lengths = [3, 4, 5, 6, 25, 50, 100]
        ids_per_length = 25

        for length in ids_lengths:
            print('')
            print('Testing ids with length=' + str(length))
            print('')
            for i in range(1, ids_per_length + 1):
                id = Id.random(length)
                print('Checking id=' + str(id), end=" ")
                check_id(self=self, id=id)
                print('OK')

    def test_mutate(self):
        ids_lengths = [6, 10, 25, 50, 100]
        ids_per_length = 20
        mutations_per_id = 40

        for length in ids_lengths:
            for i in range(1, ids_per_length + 1):
                id = Id.random(length)
                print('Testing ' + str(mutations_per_id) + ' mutations on id #' + str(
                    i) + ' ' + str(id) + ' of length ' + str(length) + '...')
                for t in range(mutations_per_id):
                    prev_id = id.copy()
                    id, pos, char_to_mutate, char_to_mutate_to = id.mutate(additional_data=True)
                    # final_id = id.mutate(True)
                    check_id(self=self, id=id, pos_to_mutate=pos, char_to_mutate=char_to_mutate,
                             char_to_mutate_to=char_to_mutate_to)
                    # check_id(self=self, id=final_id)
                    print('  ' + str(prev_id) + " -> " + str(id) + " OK  pos=" + str(pos) + "  char_to_mutate=" +
                          char_to_mutate + "  char_to_mutate_to=" + char_to_mutate_to + "  length=" + str(len(id)))


if __name__ == "__main__":
    unittest.main()
