import unittest
from metrics_calculator.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator


class DegreeAndDiameterCalculatorTest(unittest.TestCase):

    def test_shortest_path_length_between_two_nodes(self):

        all_3 = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        square = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
        all_4 = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]

        func = DegreeAndDiameterCalculator.shortest_path_length_between_two_nodes

        # On any all-connected matrix, all shortest paths should be length=1
        self.assertEqual(func(all_3, 0, 1), 1)
        self.assertEqual(func(all_3, 0, 2), 1)
        self.assertEqual(func(all_3, 1, 2), 1)

        # TODO


if __name__ == "__main__":
    unittest.main()
