import unittest
from topology_manager.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator


class AdjacencyMatrixGeneratorTest(unittest.TestCase):

    def test_is_matrix_connected(self):

        func = AdjacencyMatrixGenerator.is_matrix_connected

        self.assertTrue(func([0]))
        self.assertTrue(func([[0, 1], [1, 0]]))
        self.assertTrue(func([[0, 1, 1], [1, 0, 1], [1, 1, 0]]))
        self.assertTrue(func([[0, 1, 0], [1, 0, 1], [0, 1, 0]]))
        self.assertTrue(func([[0, 1, 0, 0], [1, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 0]]))

        self.assertFalse(func([[0, 1, 0], [1, 0, 0], [0, 0, 0]]))
        self.assertFalse(func([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))
        self.assertFalse(func([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))


if __name__ == "__main__":
    unittest.main()
