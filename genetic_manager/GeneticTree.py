import math
from misc.config import max_number_of_children
from topology_manager.IdMutator import IdMutator
from score.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator
from topology_manager.AdjacencyMatrixGenerator import AdjacencyMatrixGenerator


class GeneticTree:

    def __init__(self, id: str, iteration: int = -1, children=None, degree: int = -1, diameter: int = -1,
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

    def get_last_child(self, parent=None):
        if len(self.children) > 0:
            best_child = None
            best_parent = None
            for child in self.children:
                new_child, new_parent = child.get_last_child(self)
                if best_child is None or best_child.is_score_better_than_self(new_child.score()):
                    best_child = new_child
                    best_parent = new_parent
            return best_child, best_parent
        return self, parent

    def score(self):
        return [self.degree, self.diameter, self.score1, 0]

    def number_of_mutations(self):
        number = (int(int(math.sqrt(self.iteration - self.__initial_iteration)) / 2)) - len(self.children)
        return 1 if number <= 0 else number

    def is_score_better_than_self(self, score):
        score0 = self.score0
        new_score0 = score[0] + score[1]
        score1_better_than_actual = score[2] + score[3] < self.score1
        return new_score0 < score0 or (new_score0 == score0 and score1_better_than_actual)

    def is_score_equal_than_self(self, score):
        new_score0 = score[0] + score[1]
        score1_equal_than_actual = score[2] + score[3] == self.score1
        return new_score0 == self.score0 and score1_equal_than_actual

    def is_score_better_than_children(self, score):
        new_score0 = score[0] + score[1]
        for child in self.children:
            child_score0 = child.score0
            if child_score0 < new_score0 or (child_score0 == new_score0 and child.score1 <= score[2] + score[3]):
                return False
        return True

    def is_score_equal_than_children(self, score):
        new_score0 = score[0] + score[1]
        for child in self.children:
            child_score0 = child.score0
            if child_score0 != new_score0 or (child_score0 == new_score0 and child.score1 != score[2] + score[3]):
                return False
        return True

    def get_children_ids(self):
        ids = []
        for child in self.children:
            ids.append(child.id)
        return ids

    def mutate(self, child: bool = True):
        self.iteration += 1
        number_of_mutations = self.number_of_mutations()
        mutated_id = self.id
        for i in range(number_of_mutations):
            mutated_id, matrix = IdMutator.mutate_to_connected_matrix_id(mutated_id,
                                                                         prohibited_ids=self.get_children_ids())
            score = DegreeAndDiameterCalculator.calculate(matrix)
            score_better_than_self = self.is_score_better_than_self(score)
            score_equal_than_self = self.is_score_equal_than_self(score)
            if score_better_than_self or score_equal_than_self:
                new_tree = GeneticTree(mutated_id, degree=score[0], diameter=score[1], score1=score[2] + score[3],
                                       iteration=self.iteration)
                if score_better_than_self:
                    score_better_than_children = self.is_score_better_than_children(score)
                    score_equal_than_children = self.is_score_equal_than_children(score)
                    if score_equal_than_children or score_better_than_children:
                        self.__initial_iteration = self.iteration
                        if score_better_than_children:
                            self.children = [new_tree]
                        elif len(self.children) < max_number_of_children:
                            self.children.append(new_tree)
                        return new_tree, True
                elif len(self.children) <= 0 and child:
                    self.__initial_iteration = self.iteration
                    return new_tree, False
        return self, False

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
