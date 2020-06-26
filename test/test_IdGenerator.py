import unittest

from main.IdGenerator import IdGenerator
from symbols.interpretable_symbol.functions.operators.Operator import Operator
from symbols.Symbol import Symbol


def check_id(self, id, pos_to_mutate: int = -1, char_to_mutate: str = '', char_to_mutate_to: str = '', prefix: str = '',
             suffix: str = '', check_parenthesis: bool = True):
    id_len = len(id)
    symbols = []
    prev_char = None
    for char in id:
        symbol = Symbol.parse(char, prev_number_or_symbol=prev_char)
        symbols.append(symbol)
        prev_char = symbol
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
    if check_parenthesis:
        self.assertEqual(parenthesis_counter, 0, "Incorrect number of parenthesis.")
    self.assertFalse(id[id_len - 1] in Operator.operators(), "Id ends with an invalid character.")


class IdGeneratorTest(unittest.TestCase):

    def test_stress_generation(self):
        ids_lengths = [3, 5, 10, 25, 100]
        ids_per_length = 20

        for length in ids_lengths:
            print('')
            print('Testing ids with length=' + str(length))
            print('')
            for i in range(1, ids_per_length + 1):
                id = IdGenerator.generate_id(length)
                print('Checking id=' + id, end=" ")
                check_id(self=self, id=id)
                print('OK')


if __name__ == "__main__":
    unittest.main()
