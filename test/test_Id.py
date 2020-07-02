import unittest


from test.test_IdGenerator import check_id
from symbols.Id import Id


class IdTest(unittest.TestCase):

    def test_random(self):
        ids_lengths = [3, 4, 5, 6, 25, 100]
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


if __name__ == "__main__":
    unittest.main()
