import sys
from datetime import datetime
from misc.config import save_results_frequency
from misc.config import max_number_of_children
from misc.ResultsManager import ResultsManager
from genetic_manager.GeneticTree import GeneticTree
from topology_manager.IdGenerator import IdGenerator


class GeneticTreeManager:

    initial_trees = []
    trees = []
    number_of_iterations = 0
    winning_tree = None
    iterations_when_last_saved = 0
    results_file_name = None

    @staticmethod
    def save_tree_list():
        if GeneticTreeManager.results_file_name is None:
            GeneticTreeManager.results_file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        str_to_write = "[\n\t"
        for i in range(len(GeneticTreeManager.initial_trees)):
            if i > 0:
                str_to_write += ", \n\t"
            str_to_write += GeneticTreeManager.initial_trees[i].to_json()
        str_to_write += "\n]"
        ResultsManager.write_results(GeneticTreeManager.results_file_name, str_to_write)

    @staticmethod
    def print_successful_mutation(father_or_child: str, tree, new_tree, j):
        print(" " + father_or_child + " Tree " + str(j) + ":  " + tree.id + "  (degree=" + str(tree.degree) +
              ", diameter=" + str(tree.diameter) + ", score1=" + str(tree.score1) + ") mutated to  " + new_tree.id +
              "  (degree=" + str(new_tree.degree) + ", diameter=" + str(new_tree.diameter) + ", score1=" +
              str(new_tree.score1) + ")")

    @staticmethod
    def run(iterations: int, number_of_trees: int, trees_list: list = None):
        if number_of_trees <= 0:
            number_of_trees = 1
        # TODO: Implement GenericTree.parent attribute in order to remove initial_trees list.
        if len(GeneticTreeManager.initial_trees) == 0 or (trees_list is not None and len(trees_list) > 0):
            if trees_list:
                GeneticTreeManager.initial_trees = trees_list
            while len(GeneticTreeManager.initial_trees) < number_of_trees:
                new_tree = GeneticTree(IdGenerator.generate_connected_matrix_id())
                GeneticTreeManager.initial_trees.append(new_tree)
            GeneticTreeManager.trees = []
            for tree in GeneticTreeManager.initial_trees:
                # This two next lines assure us that the actual trees will be the penultimate trees of the initial trees
                last_child, parent = tree.get_last_child()
                GeneticTreeManager.trees.append(parent if parent else last_child)
        final_number_of_iterations = GeneticTreeManager.number_of_iterations + iterations

        for i in range(GeneticTreeManager.number_of_iterations, final_number_of_iterations):
            print("Iteration " + str(i) + "/" + str(final_number_of_iterations - 1) + "...")
            sys.stdout.flush()
            for j in range(len(GeneticTreeManager.trees)):
                tree = GeneticTreeManager.trees[j]
                no_child_mutated = True
                child_mutated_to_equal_pair = None
                for child in tree.children:
                    new_tree, is_better_than_child = child.mutate()
                    if new_tree != child:
                        new_child_not_in_children = new_tree.id not in tree.get_children_ids()
                        if is_better_than_child or new_child_not_in_children:
                            if is_better_than_child:
                                GeneticTreeManager.trees[j] = child
                                GeneticTreeManager.print_successful_mutation("Child", child, new_tree, j)
                                sys.stdout.flush()
                                no_child_mutated = False
                                break
                            else:
                                child_mutated_to_equal_pair = [child, new_tree]
                if no_child_mutated:
                    if child_mutated_to_equal_pair and len(tree.children) < max_number_of_children:
                        GeneticTreeManager.print_successful_mutation("Child (E)", child_mutated_to_equal_pair[0],
                                                                     child_mutated_to_equal_pair[1], j)
                        sys.stdout.flush()
                        GeneticTreeManager.trees[j].children.append(child_mutated_to_equal_pair[1])
                    else:
                        new_tree, is_better_than_child = tree.mutate(False)
                        # In this case, is_better_than_child variable does not represent anything,
                        # given we are not a child but the father
                        if new_tree != tree:
                            GeneticTreeManager.print_successful_mutation("Father", tree, new_tree, j)
                            sys.stdout.flush()
            if 0 < i < final_number_of_iterations - 1 and i % save_results_frequency == 0:
                print(" Auto-saving results... (Actual saving frequency: " + str(save_results_frequency) + " iterations)")
                GeneticTreeManager.save_tree_list()
            GeneticTreeManager.number_of_iterations += 1
        print(" Saving final results...")
        GeneticTreeManager.save_tree_list()
