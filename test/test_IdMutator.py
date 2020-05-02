import unittest
from IdGenerator import IdGenerator
import random
from IdMutator import IdMutator
from global_variables import *


class IdMutatorTest(unittest.TestCase):

    @staticmethod
    def generate_id_and_get_char_to_mutate_to(id_mutator: IdMutator, id_length: int):
        new_id = IdGenerator.generate_id(id_length)
        id_mutator.set_id_and_wanted_length(new_id, len(new_id))
        id_mutator.calculate_pos_to_mutate()
        chars_available_to_mutate_to = id_mutator.get_chars_available_to_mutate_to()
        return chars_available_to_mutate_to[random.randint(0, len(chars_available_to_mutate_to) - 1)]

    def test__clean_char_to_mutate_to(self):

        id_mutator = IdMutator()
        char_to_mutate_to = IdMutatorTest.generate_id_and_get_char_to_mutate_to(id_mutator, 10)
        # TODO

    def test_stress_mutate(self):

        ids_lengths = [3, 5, 10, 25, 100]
        number_of_mutation_per_id = 10
        ids_per_length = 4
        id_mutator = IdMutator()

        for length in ids_lengths:
            for i in range(1, ids_per_length + 1):
                id = IdGenerator.generate_id(length)
                print('Testing ' + str(number_of_mutation_per_id) + ' mutations on id #' + str(
                    i) + ' (' + id + ') of length ' + str(length) + '...', end=" ")
                for i in range(number_of_mutation_per_id):
                    mutated_id, pos, c, new_c = id_mutator.mutate_id(id, length)
                    mutated_id_len = len(mutated_id)
                    parenthesis_counter = 0
                    for j in range(mutated_id_len):
                        if mutated_id[j] == '(':
                            parenthesis_counter += 1
                        elif mutated_id[j] == ')':
                            self.assertNotEqual(parenthesis_counter, 0,
                                                "Found close parenthesis when there's no open parenthesis to close.")
                            parenthesis_counter -= 1
                        error = ''
                        if j > 0 and mutated_id[j - 1] in forbidden_left_chars[mutated_id[j]]:
                            error = 'L'
                        elif j + 1 < mutated_id_len and mutated_id[j + 1] in forbidden_right_chars[mutated_id[j]]:
                            error = 'R'
                        if error != '':
                            print('')
                            print(mutated_id)
                            print((' ' * j) + '^ char \'' + mutated_id[j] + '\' must not be ' + (
                                'preceded' if error == 'L' else 'followed') + ' by char \'' + mutated_id[
                                      j + (-1 if error == 'L' else 1)] + '\'')
                            self.assertTrue(False)  # We use this assert only to stop the test.
                    self.assertNotEqual(parenthesis_counter, 0, "Incorrect number of parenthesis.")


if __name__ == "__main__":
    unittest.main()
