from topology_manager.ExpressionInterpreter import ExpressionInterpreter
from id_manager.IdGenerator import IdGenerator


class AdjacencyMatrixGenerator:

    @staticmethod
    def compute(id, n):
        adj_matrix = []
        str_n = str(n)
        for x in range(0, n):
            adj_matrix.append([0] * n)
        for x in range(0, n):
            str_x = str(x)
            for y in range(x+1, n):
                str_y = str(y)
                expression = id.replace("x", str_x).replace("y", str_y).replace("n", str_n)
                result = round(ExpressionInterpreter.compute(expression))
                if result > 0:
                    adj_matrix[x][y] = 1
                    adj_matrix[y][x] = 1
        return adj_matrix


if __name__ == '__main__':
    AdjacencyMatrixGenerator.compute(IdGenerator.generate_id(20), 10)
