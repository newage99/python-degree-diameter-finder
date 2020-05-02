import unittest
from IdGenerator import IdGenerator
import random
from IdMutator import IdMutator


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


if __name__ == "__main__":
    unittest.main()
