import unittest

from classes.interpretable_symbols.functions.operators.Operator import Operator
from classes.Symbol import Symbol
from classes.Id import Id


def check_id(self, id, pos_to_mutate: int = -1, char_to_mutate: str = '', char_to_mutate_to: str = '', prefix: str = '',
             suffix: str = ''):
    error = id.check()
    if error:
        print(id + ' pos_to_mutate=' + str(pos_to_mutate) + ', char_to_mutate=' + char_to_mutate +
              ', char_to_mutate_to=' + char_to_mutate_to + ', prefix=' + prefix + ', suffix=' + suffix)
        print(error)
        self.assertTrue(False)


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
