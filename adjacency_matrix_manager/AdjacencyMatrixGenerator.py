from adjacency_matrix_manager.mathematical_expression_interpreter.MathematicalExpressionInterpreter import ExpressionInterpreter
from misc.config import number_of_nodes
from topology_manager.IdGenerator import IdGenerator
import networkx


class AdjacencyMatrixGenerator:

    @staticmethod
    def is_matrix_connected(matrix):
        graph = networkx.Graph()
        n = len(matrix)
        for x in range(0, n):
            graph.add_node(x)
        for x in range(0, n):
            for y in range(x + 1, n):
                if matrix[x][y]:
                    graph.add_edge(x, y)
        components = networkx.algorithms.components.connected.connected_components(graph)
        number_of_components = 0
        first_component_length = 0
        for c in components:
            first_component_length = len(c)
            number_of_components += 1
            if number_of_components >= 2:
                break
        return number_of_components == 1 and first_component_length == n

    @staticmethod
    def generate_and_get_if_its_connected(id, n=number_of_nodes):
        matrix = []
        str_n = str(n)
        for x in range(0, n):
            matrix.append([0] * n)
        for x in range(0, n):
            str_x = str(x)
            for y in range(x + 1, n):
                str_y = str(y)
                expression = id.replace("x", str_x).replace("y", str_y).replace("n", str_n)
                result = round(ExpressionInterpreter.compute(expression))
                if result > 0:
                    matrix[x][y] = matrix[y][x] = 1
        return matrix, AdjacencyMatrixGenerator.is_matrix_connected(matrix)


if __name__ == '__main__':
    # Way to easily debug function
    AdjacencyMatrixGenerator.generate_and_get_if_its_connected(IdGenerator.generate_id(20), 5)
