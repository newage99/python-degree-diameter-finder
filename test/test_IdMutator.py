import unittest

from main.IdMutator import IdMutator
from symbols.Id import Id
from test.test_Id import check_id


class IdMutatorTest(unittest.TestCase):

    def perform_mutation_stress_test(self):

        ids_lengths = [5, 10, 25, 100]
        number_of_mutation_per_id = 50
        ids_per_length = 20

        for length in ids_lengths:
            for i in range(1, ids_per_length + 1):
                id = str(Id.random(length))
                print('Testing ' + str(number_of_mutation_per_id) + ' mutations on id #' + str(
                    i) + ' ' + id + ' of length ' + str(length) + '...', end=" ")
                for t in range(number_of_mutation_per_id):
                    final_id, pos, char_to_mutate, char_to_mutate_to, prefix, suffix = IdMutator.mutate_id(id, True)
                    check_id(self=self, id=final_id, pos_to_mutate=pos, char_to_mutate=char_to_mutate,
                             char_to_mutate_to=char_to_mutate_to, prefix=prefix, suffix=suffix)
                print('OK')

    def test_mutate_id(self):
        self.perform_mutation_stress_test()


if __name__ == "__main__":
    unittest.main()
