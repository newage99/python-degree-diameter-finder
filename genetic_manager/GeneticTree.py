import math
from topology_manager.IdMutator import IdMutator
from score.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator
from adjacency_matrix_manager.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator


class GeneticTree:

    def __init__(self, id: str, iteration: int = 0, children=None, degree: int = -1, diameter: int = -1,
                 score1: int = -1):
        self.id = id
        self.__initial_iteration = iteration
        self.iteration = iteration
        self.children = children if children else []
        self.degree = degree
        self.diameter = diameter
        self.score1 = score1
        if degree == -1:
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(id)
            score = DegreeAndDiameterCalculator.calculate(matrix)
            self.degree = score[0]
            self.diameter = score[1]
            self.score1 = score[2] + score[3]

    @property
    def score0(self):
        return self.degree + self.diameter

    def get_last_child(self):
        return self if len(self.children) <= 0 else self.children[0].get_last_child()

    def number_of_mutations(self):
        number = int(int(math.sqrt(self.iteration - self.__initial_iteration)) / 2)
        return 1 if number <= 0 else number

    def is_score_better_than_actual(self, score):
        degree_plus_diameter = self.degree + self.diameter
        new_degree_plus_diameter = score[0] + score[1]
        return new_degree_plus_diameter < degree_plus_diameter or (
                    new_degree_plus_diameter == degree_plus_diameter and score[2] + score[3] < self.score1)

    def mutate(self):
        number_of_mutations = self.number_of_mutations()
        mutated_id = self.id
        for i in range(number_of_mutations):
            mutated_id, matrix = IdMutator.mutate_to_connected_matrix_id(mutated_id)
            score = DegreeAndDiameterCalculator.calculate(matrix)
            if self.is_score_better_than_actual(score):
                new_tree = GeneticTree(mutated_id, degree=score[0], diameter=score[1], score1=score[2] + score[3],
                                       iteration=self.iteration + 1)
                self.children.append(new_tree)
                return new_tree
        self.iteration += 1
        return self

    @staticmethod
    def from_dict(obj):
        degree = obj['degree'] if 'degree' in obj else -1
        diameter = obj['diameter'] if 'diameter' in obj else -1
        score1 = obj['score1'] if 'score1' in obj else -1
        iteration = obj['iteration'] if 'iteration' in obj else 0
        children = []
        if 'children' in obj and len(obj['children']) > 0:
            for child in obj['children']:
                children.append(GeneticTree.from_dict(child))
        return GeneticTree(id=obj['id'], iteration=iteration, children=children, degree=degree, diameter=diameter,
                           score1=score1)

    def to_json(self, indentation_exponent=1):
        indent = '\t' * indentation_exponent
        ret = "{\n" + indent + '"id": "' + self.id + '",\n' + indent + '"iteration": ' + str(
            self.iteration) + ",\n" + indent + '"degree": ' + str(self.degree) + ",\n" + indent + '"diameter": ' + str(
            self.diameter) + ",\n" + indent + '"score1": ' + str(self.score1) + ",\n" + indent + '"children": ['
        if len(self.children) > 0:
            ret += "\n" + indent + "\t"
            for i in range(len(self.children)):
                if i > 0:
                    ret += ", "
                ret += self.children[i].to_json(indentation_exponent + 1)
            ret += "\n" + indent
        return ret + "]\n" + indent + "}"
