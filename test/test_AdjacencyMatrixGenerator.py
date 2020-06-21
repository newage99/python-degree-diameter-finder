import unittest
from main.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator


class AdjacencyMatrixGeneratorTest(unittest.TestCase):

    def test_is_matrix_connected(self):

        matrix_connected = AdjacencyMatrixGenerator.is_matrix_connected

        self.assertTrue(matrix_connected([0]))
        self.assertTrue(matrix_connected([[0, 1], [1, 0]]))
        self.assertTrue(matrix_connected([[0, 1, 1], [1, 0, 1], [1, 1, 0]]))
        self.assertTrue(matrix_connected([[0, 1, 0], [1, 0, 1], [0, 1, 0]]))
        self.assertTrue(matrix_connected([[0, 1, 0, 0], [1, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 0]]))

        self.assertFalse(matrix_connected([[0, 1, 0], [1, 0, 0], [0, 0, 0]]))
        self.assertFalse(matrix_connected([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))
        self.assertFalse(matrix_connected([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))


if __name__ == "__main__":
    unittest.main()
