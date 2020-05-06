

class DegreeAndDiameterCalculator:

    @staticmethod
    def shortest_path_length_between_two_nodes(matrix, a, b):
        diameter_add_position = 0
        to_visit_counter = 0
        to_visit = [a]
        len_matrix = len(matrix)
        diameter = 0
        while to_visit_counter < len(to_visit) < len_matrix:
            actual_node_neighbours = matrix[to_visit[to_visit_counter]]
            nodes_to_check = []
            for i in range(0, len(actual_node_neighbours)):
                if actual_node_neighbours[i] > 0 and i not in to_visit:
                    nodes_to_check.append(i)
            for node_to_check in nodes_to_check:
                if node_to_check == b:
                    return diameter + 1
                to_visit.append(node_to_check)
            if to_visit_counter == diameter_add_position:
                diameter_add_position = len(to_visit) - 1
                diameter += 1
            to_visit_counter += 1
        return -1

    @staticmethod
    def calculate(matrix):

        len_matrix = len(matrix)
        number_of_neighbours = {}
        for i in range(0, len_matrix):
            number_of_neighbours[i] = sum(matrix[i])

        degree = 0
        diameter = 0
        total_degree = 0
        total_diameter = 0

        for x in range(0, len_matrix):
            for y in range(x+1, len_matrix):
                actual_degree = (number_of_neighbours[x] + number_of_neighbours[y]) / 2
                actual_diameter = DegreeAndDiameterCalculator.shortest_path_length_between_two_nodes(matrix, x, y)
                if actual_diameter == -1:
                    # This means dijkstra has not found a path between the two nodes, so the matrix is not connected.
                    return [-1, -1, -1, -1]
                total_degree += degree
                total_diameter += diameter
                if actual_degree > degree:
                    degree = actual_degree
                if actual_diameter > diameter:
                    diameter = actual_diameter

        return [degree, diameter, total_degree, total_diameter]
