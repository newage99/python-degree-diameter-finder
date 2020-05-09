import json
import math
from topology_manager.IdMutator import IdMutator
from score.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator
from adjacency_matrix_manager.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator


class GeneticTree:

    def __init__(self, id, children=None, matrix=None):
        self.id = id
        if matrix is None:
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(id)
        score = DegreeAndDiameterCalculator.calculate(matrix)
        self.degree = score[0]
        self.diameter = score[1]
        self.score1 = score[2] + score[3]
        self.mutation_tries = 0
        self.children = children if children else []
        self.__already_created_counter = 0

    @property
    def score0(self):
        return self.degree + self.diameter

    def number_of_mutations(self):
        number = int(int(math.sqrt(self.mutation_tries)) / 2)
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
                new_tree = GeneticTree(mutated_id, matrix=matrix)
                self.children.append(new_tree)
                return new_tree
        self.mutation_tries += 1
        return self

    @staticmethod
    def load(json):
        try:
            def from_json(obj):
                if 'id' in obj:
                    children = obj.children if 'children' in obj and len(obj.children) > 0 else []
                    return GeneticTree(id=obj['id'], children=children)
            result = json.JSONDecoder(object_hook=from_json).decode(json)
            return result is not None
        except Exception as e:
            return False

    def to_json(self, indentation_exponent=1):
        indentation_str = '\t\t' * indentation_exponent
        ret = "{\n" + indentation_str + '"id": "' + self.id + '",\n' + indentation_str + '"degree": ' + str(self.degree)
        ret += ",\n" + indentation_str + '"diameter": ' + str(self.diameter) + ",\n" + indentation_str
        ret += '"score1": ' + str(self.score1) + ",\n" + indentation_str + '"children": ['
        if len(self.children) > 0:
            ret += "\n" + indentation_str + "\t"
            for i in range(len(self.children)):
                if i > 0:
                    ret += ", "
                ret += self.children[i].to_json(indentation_exponent + 1)
            ret += "\n" + indentation_str
        return ret + "]\n\t" + ('\t\t' * (indentation_exponent - 1)) + "}"
