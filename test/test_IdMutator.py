import unittest
from IdGenerator import IdGenerator
import random
from IdMutator import IdMutator
from global_variables import *


class IdMutatorTest(unittest.TestCase):

    id_mutator = None

    def calculate_char_to_mutate_and_return_cleaned_id_and_data(self, new_id):
        self.id_mutator.set_id_and_wanted_length(new_id, len(new_id))
        self.id_mutator.calculate_pos_to_mutate()
        pos_to_mutate = self.id_mutator.pos_to_mutate
        chars_available_to_mutate_to = self.id_mutator.get_chars_available_to_mutate_to()
        char_to_mutate_to = chars_available_to_mutate_to[random.randint(0, len(chars_available_to_mutate_to) - 1)]
        prefix, char_to_mutate_to, suffix = self.id_mutator.clean_char_to_mutate_to(char_to_mutate_to)
        cleaned_id = new_id[:pos_to_mutate] + prefix + char_to_mutate_to + suffix + new_id[pos_to_mutate + 1:]
        return cleaned_id, new_id, pos_to_mutate, self.id_mutator.char_to_mutate, char_to_mutate_to

    def check_id(self, id, old_id, pos_to_mutate, char_to_mutate, char_to_mutate_to, check_parenthesis: bool = True):

        id_len = len(id)
        parenthesis_counter = 0
        for j in range(id_len):
            if id[j] == '(':
                parenthesis_counter += 1
            elif id[j] == ')':
                if check_parenthesis:
                    self.assertNotEqual(parenthesis_counter, 0,
                                        "Found close parenthesis when there's no open parenthesis to close.")
                parenthesis_counter -= 1
            error = ''
            if j > 0 and id[j - 1] in forbidden_left_chars[id[j]]:
                error = 'L'
            elif j + 1 < id_len and id[j + 1] in forbidden_right_chars[id[j]]:
                error = 'R'
            if error != '':
                print('')
                print(id + ' pos_to_mutate=' + str(
                    pos_to_mutate) + ', char_to_mutate=' + char_to_mutate + ', char_to_mutate_to=' + char_to_mutate_to)
                print((' ' * j) + '^ char \'' + id[j] + '\' must not be ' + (
                    'preceded' if error == 'L' else 'followed') + ' by char \'' + id[
                          j + (-1 if error == 'L' else 1)] + '\'')
                self.assertTrue(False)  # We use this assert only to stop the test.
        if check_parenthesis:
            self.assertNotEqual(parenthesis_counter, 0, "Incorrect number of parenthesis.")

    def perform_mutation_stress_test(self, function_to_call, check_parenthesis):

        ids_lengths = [3, 5, 10, 25, 100]
        number_of_mutation_per_id = 2000
        ids_per_length = 12
        self.id_mutator = IdMutator()

        for length in ids_lengths:
            for i in range(1, ids_per_length + 1):
                id = IdGenerator.generate_id(length)
                print('Testing ' + str(number_of_mutation_per_id) + ' mutations on id #' + str(
                    i) + ' ' + id + ' of length ' + str(length) + '...', end=" ")
                for t in range(number_of_mutation_per_id):
                    final_id, id, pos_to_mutate, char_to_mutate, char_to_mutate_to = function_to_call(id)
                    self.check_id(id=final_id, old_id=id, pos_to_mutate=pos_to_mutate, char_to_mutate=char_to_mutate,
                                  char_to_mutate_to=char_to_mutate_to, check_parenthesis=check_parenthesis)
                print('OK')

    def test__clean_char_to_mutate_to(self):
        self.perform_mutation_stress_test(self.calculate_char_to_mutate_and_return_cleaned_id_and_data, False)

    def test_mutate_id(self):
        pass
        # self.perform_mutation_stress_test(self.id_mutator.mutate_id, True)


if __name__ == "__main__":
    unittest.main()
