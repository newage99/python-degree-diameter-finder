import unittest
from score.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator


class DegreeAndDiameterCalculatorTest(unittest.TestCase):

    # calculate = DegreeAndDiameterCalculator.calculate

    # Custom matrix in order to better test the functions:
    #
    #      1---2-----5
    #     /     \    |
    #    0       3---4---6
    #     \     /
    #      9---7---8
    #
    custom = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 1, 0, 0]]

    custom_distance_1_pairs = [[0, 1], [0, 9], [1, 2], [2, 3], [2, 5], [3, 4], [3, 7], [4, 5], [4, 6], [7, 8], [7, 9]]
    custom_distance_2_pairs = [[0, 2], [0, 7], [1, 3], [1, 5], [1, 9], [2, 4], [2, 7], [3, 5], [3, 6], [3, 8], [3, 9],
                               [4, 7], [5, 6], [8, 9]]
    custom_distance_3_pairs = [[0, 3], [0, 5], [0, 8], [1, 4], [1, 7], [2, 6], [2, 8], [2, 9], [4, 8], [4, 9], [5, 7],
                               [6, 7]]
    custom_distance_4_pairs = [[0, 4], [1, 6], [1, 8], [5, 8], [5, 9], [6, 8], [6, 9]]

    @staticmethod
    def triangular_neighbours(matrix):
        len_matrix = len(matrix)
        number_of_neighbours = {}
        for i in range(0, len_matrix):
            number_of_neighbours[i] = sum(matrix[i])
        n = 0
        for x in range(0, len_matrix):
            for y in range(x+1, len_matrix):
                n += (number_of_neighbours[x] + number_of_neighbours[y]) / 2
        return n

    @staticmethod
    def triangular(n):
        return (n*(n-1)) / 2

    @staticmethod
    def create_fully_connected_matrix(size):
        matrix = []
        for i in range(size):
            matrix.append([1] * size)
            matrix[i][i] = 0
        return matrix

    def check_paths_list(self, matrix: list, path_list: list, length: int):
        for i in range(len(path_list)):
            self.assert_shortest_path_length(matrix, path_list[i][0], path_list[i][1], length)

    def assert_shortest_path_length(self, matrix: list, a: int, b: int, length: int):
        self.assertEqual(DegreeAndDiameterCalculator.shortest_path_length_between_two_nodes(matrix, a, b), length)

    def create_and_check_fully_connected_matrix(self, size: int):
        matrix = DegreeAndDiameterCalculatorTest.create_fully_connected_matrix(size)
        for a in range(3):
            for b in range(a + 1, 3):
                self.assert_shortest_path_length(matrix, a, b, 1)

    def test_shortest_path_length_between_two_nodes(self):

        # On any all-connected matrix, all shortest paths should be length=1
        self.create_and_check_fully_connected_matrix(3)
        self.create_and_check_fully_connected_matrix(6)
        self.create_and_check_fully_connected_matrix(11)

        square = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]

        # On square matrix, the shortest path between opposite nodes should be length=2
        self.check_paths_list(square, [[0, 2], [1, 3]], 2)
        # and adjacent nodes length=1
        self.check_paths_list(square, [[0, 1], [0, 3], [1, 2], [2, 3]], 1)

        # On the custom matrix, we first we check adjacent nodes...
        self.check_paths_list(self.custom, self.custom_distance_1_pairs, 1)
        # then we check node pair at distance 2...
        self.check_paths_list(self.custom, self.custom_distance_2_pairs, 2)
        # distance 3...
        self.check_paths_list(self.custom, self.custom_distance_3_pairs, 3)
        # distance 4...
        self.check_paths_list(self.custom, self.custom_distance_4_pairs, 4)
        # and finally distance 5 (the matrix diameter)
        self.assert_shortest_path_length(self.custom, 0, 6, 5)

    def check_calculate_on_fully_connected_matrix(self, size):
        matrix = DegreeAndDiameterCalculatorTest.create_fully_connected_matrix(size)
        triangular_size = DegreeAndDiameterCalculatorTest.triangular(size)
        calculate = DegreeAndDiameterCalculator.calculate
        self.assertEqual(calculate(matrix), [size - 1, 1, (size-1) * triangular_size, triangular_size])

    def test_calculate(self):

        self.check_calculate_on_fully_connected_matrix(4)
        self.check_calculate_on_fully_connected_matrix(9)
        self.check_calculate_on_fully_connected_matrix(11)

        total_diameter = len(self.custom_distance_1_pairs) + (len(self.custom_distance_2_pairs) * 2) + (
                    len(self.custom_distance_3_pairs) * 3) + (len(self.custom_distance_4_pairs) * 4) + 5
        total_degree = DegreeAndDiameterCalculatorTest.triangular_neighbours(self.custom)
        calculate = DegreeAndDiameterCalculator.calculate
        self.assertEqual(calculate(self.custom), [3, 5, total_degree, total_diameter])


if __name__ == "__main__":
    unittest.main()
