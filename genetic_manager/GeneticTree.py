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
        self.score = score[2] + score[3]
        self.mutation_tries = 0
        self.children = children if children else []
        self.__already_created_counter = 0

    def number_of_mutations(self):
        number = int(int(math.sqrt(self.mutation_tries)) / 2)
        return 1 if number <= 0 else number

    @staticmethod
    def mutate_id_until_matrix_is_connected(id):
        connected = False
        while not connected:
            mutated_id = IdMutator.mutate_id(id)
            matrix, connected = AdjacencyMatrixGenerator.generate_and_get_if_its_connected(mutated_id)
        return mutated_id, matrix

    def is_score_better_than_actual(self, score):
        degree_plus_diameter = self.degree + self.diameter
        new_degree_plus_diameter = score[0] + score[1]
        return new_degree_plus_diameter < degree_plus_diameter or (
                    new_degree_plus_diameter == degree_plus_diameter and score[2] + score[3] < self.score)

    def mutate(self):
        number_of_mutations = self.number_of_mutations()
        mutated_id = self.id
        not_mutated = True
        for i in range(number_of_mutations):
            mutated_id, matrix = GeneticTree.mutate_id_until_matrix_is_connected(mutated_id)
            score = DegreeAndDiameterCalculator.calculate(matrix)
            if self.is_score_better_than_actual(score):
                self.children.append(GeneticTree(mutated_id, matrix=matrix))
                not_mutated = False
                break
        if not_mutated:
            self.mutation_tries += 1

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

    def dump(self):
        return json.dumps(self.__dict__)
