import networkx

from classes.Id import Id
from main.ExpressionInterpreter import ExpressionInterpreter
from misc.config import number_of_nodes


class AdjacencyMatrix:

    def __init__(self, matrix: list):
        self.__matrix = matrix
        self.__is_connected = None
        self.is_connected()

    def is_connected(self):
        if self.__is_connected is None:
            graph = networkx.Graph()
            n = len(self.__matrix)
            for x in range(0, n):
                graph.add_node(x)
            for x in range(0, n):
                for y in range(x + 1, n):
                    if self.__matrix[x][y]:
                        graph.add_edge(x, y)
            components = networkx.algorithms.components.connected.connected_components(graph)
            number_of_components = 0
            first_component_length = 0
            for c in components:
                first_component_length = len(c)
                number_of_components += 1
                if number_of_components >= 2:
                    break
            self.__is_connected = number_of_components == 1 and first_component_length == n
        return self.__is_connected

    @staticmethod
    def create_unconnected_matrix():
        return AdjacencyMatrix([[0, 0], [0, 0]])

    @staticmethod
    def parse(id: Id, n: int = number_of_nodes):
        matrix = []
        str_n = str(n)
        for x in range(0, n):
            matrix.append([0] * n)
        for x in range(0, n):
            str_x = str(x)
            for y in range(x + 1, n):
                str_y = str(y)
                expression = str(id).replace("x", str_x).replace("y", str_y).replace("n", str_n)
                result = ExpressionInterpreter.compute(expression)
                if result == float("inf"):
                    result = 1
                elif result == float("-inf"):
                    result = 0
                result = round(result)
                if result > 0:
                    matrix[x][y] = matrix[y][x] = 1
        return AdjacencyMatrix(matrix)

    def __len__(self):
        return len(self.__matrix)

    def __getitem__(self, item):
        return self.__matrix[item]
