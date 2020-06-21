import unittest
from IdGenerator import IdGenerator
from IdMutator import IdMutator
from misc.global_variables import *


class IdMutatorTest(unittest.TestCase):

    def check_id(self, id, pos_to_mutate, char_to_mutate, char_to_mutate_to, prefix, suffix,
                 check_parenthesis: bool = True):

        id_len = len(id)
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
            if j > 0 and id[j - 1] in forbidden_left_chars[id[j]]:
                error = 'L'
            elif j + 1 < id_len and id[j + 1] in forbidden_right_chars[id[j]]:
                error = 'R'
            if error != '':
                print('')
                print(id + ' pos_to_mutate=' + str(pos_to_mutate) + ', char_to_mutate=' + char_to_mutate +
                      ', char_to_mutate_to=' + char_to_mutate_to + ', prefix=' + prefix + ', suffix=' + suffix)
                print((' ' * j) + '^ char \'' + id[j] + '\' must not be ' + (
                    'preceded' if error == 'L' else 'followed') + ' by char \'' + id[
                          j + (-1 if error == 'L' else 1)] + '\'')
                self.assertTrue(False)  # We use this assert only to stop the test.
        if check_parenthesis:
            self.assertEqual(parenthesis_counter, 0, "Incorrect number of parenthesis.")
        self.assertFalse(id[id_len-1] in operators, "Id ends with an invalid character.")

    def perform_mutation_stress_test(self, check_parenthesis: bool):

        ids_lengths = [3, 5, 10, 25, 100]
        number_of_mutation_per_id = 50
        ids_per_length = 20

        for length in ids_lengths:
            for i in range(1, ids_per_length + 1):
                id = IdGenerator.generate_id(length)
                print('Testing ' + str(number_of_mutation_per_id) + ' mutations on id #' + str(
                    i) + ' ' + id + ' of length ' + str(length) + '...', end=" ")
                for t in range(number_of_mutation_per_id):
                    final_id, pos, char_to_mutate, char_to_mutate_to, prefix, suffix = IdMutator.mutate_id(id, True)
                    self.check_id(id=final_id, pos_to_mutate=pos, char_to_mutate=char_to_mutate,
                                  char_to_mutate_to=char_to_mutate_to, prefix=prefix, suffix=suffix,
                                  check_parenthesis=check_parenthesis)
                print('OK')

    def test_mutate_id(self):
        self.perform_mutation_stress_test(True)


if __name__ == "__main__":
    unittest.main()
