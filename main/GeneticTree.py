import math

from main.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator
from misc.config import max_tree_ids
from classes.AdjacencyMatrix import AdjacencyMatrix
from classes.Id import Id


class GeneticTree:

    def __init__(self, ids: list, child=None, degree: int = -1, diameter: int = -1, score1: int = -1):
        self.ids = ids
        self.child = child
        if degree == -1:
            score = DegreeAndDiameterCalculator.calculate(AdjacencyMatrix.parse(ids[0]))
            degree = score[0]
            diameter = score[1]
            score1 = score[2] + score[3]
        self.degree = degree
        self.diameter = diameter
        self.score1 = score1
        self.iterations_without_change = 0

    def get_last_child(self):
        return self.child.get_last_child() if self.child else self

    def bad_score(self):
        return self.degree >= 31 and self.diameter >= 1

    @property
    def score0(self):
        return self.degree + self.diameter

    def score(self):
        return [self.degree, self.diameter, self.score1, 0]

    def is_score_better_than_self(self, score):
        score0 = self.score0
        new_score0 = score[0] + score[1]
        score1_better_than_actual = score[2] + score[3] < self.score1
        return new_score0 < score0 or (new_score0 == score0 and score1_better_than_actual)

    def is_score_equal_than_self(self, score):
        new_score0 = score[0] + score[1]
        score1_equal_than_actual = score[2] + score[3] == self.score1
        return new_score0 == self.score0 and score1_equal_than_actual

    def mutate(self):
        equal_list = []
        for i in range(len(self.ids)):
            id = self.ids[i]
            mutated_id = id.mutate()
            if mutated_id not in self.ids:
                adjacency_matrix = AdjacencyMatrix.parse(mutated_id)
                if adjacency_matrix.is_connected():
                    score = DegreeAndDiameterCalculator.calculate(adjacency_matrix)
                    if self.is_score_better_than_self(score):
                        new_tree = GeneticTree([mutated_id], degree=score[0], diameter=score[1],
                                               score1=score[2] + score[3])
                        self.child = new_tree
                        self.iterations_without_change = 0
                        return new_tree
                    elif self.is_score_equal_than_self(score):
                        equal_list.append(mutated_id)
                        print("  Id " + str(id) + " (" + str(i) + "/" + str(len(self.ids)) +
                              ") mutated to equal score id " + str(mutated_id))
        if len(equal_list) > 0:
            self.ids += equal_list
            self.iterations_without_change = 0
        else:
            self.iterations_without_change += 1
        return self

    @staticmethod
    def from_dict(obj):
        if 'ids' in obj:
            degree = obj['degree'] if 'degree' in obj else -1
            diameter = obj['diameter'] if 'diameter' in obj else -1
            score1 = obj['score1'] if 'score1' in obj else -1
            ids = [Id.parse(id) for id in obj['ids']]
            return GeneticTree(ids=ids, child=GeneticTree.from_dict(obj['child']), degree=degree, diameter=diameter,
                               score1=score1)
        return None

    def to_json(self, indentation_exponent=1):
        indent = '\t' * indentation_exponent
        ret = "{\n" + indent + '"ids": [\n' + indent + "\t"
        ids_line_break_frequency = round(math.sqrt(len(self.ids)))
        c = 0
        for i in range(len(self.ids)):
            ret += '"' + str(self.ids[i]) + '"'
            if i+1 < len(self.ids):
                ret += ", "
            if c == ids_line_break_frequency:
                ret += "\n" + indent + "\t"
                c = 0
            else:
                c += 1
        ret += "\n" + indent + '],\n' + indent + '"degree": ' + str(
            self.degree) + ",\n" + indent + '"diameter": ' + str(self.diameter) + ",\n" + indent + '"score1": ' + str(
            self.score1) + ",\n" + indent + '"child": '
        if self.child:
            ret += self.child.to_json(indentation_exponent + 1)
        else:
            ret += "{}"
        return ret + "\n" + indent + "}"
