import unittest

from classes.AdjacencyMatrix import AdjacencyMatrix


class AdjacencyMatrixTest(unittest.TestCase):

    def test_is_matrix_connected(self):

        self.assertTrue(AdjacencyMatrix([[0]]).is_connected())
        self.assertTrue(AdjacencyMatrix([[0, 1], [1, 0]]).is_connected())
        self.assertTrue(AdjacencyMatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]]).is_connected())
        self.assertTrue(AdjacencyMatrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]).is_connected())
        self.assertTrue(AdjacencyMatrix([[0, 1, 0, 0], [1, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 0]]).is_connected())

        self.assertFalse(AdjacencyMatrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]).is_connected())
        self.assertFalse(AdjacencyMatrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]).is_connected())
        self.assertFalse(AdjacencyMatrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]).is_connected())


if __name__ == "__main__":
    unittest.main()
