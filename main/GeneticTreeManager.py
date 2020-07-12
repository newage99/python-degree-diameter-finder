import sys

from datetime import datetime
from misc.config import save_results_frequency
from misc.config import iterations_without_change_before_preparing_to_delete
from misc.config import max_tree_ids
from main.ResultsManager import ResultsManager
from main.GeneticTree import GeneticTree
from classes.Id import Id


class GeneticTreeManager:

    initial_trees = []
    trees = []
    results_file_name = None

    @staticmethod
    def __init_trees(number_of_trees: int, trees_list: list = None):
        if number_of_trees <= 0:
            number_of_trees = 1
        if len(GeneticTreeManager.initial_trees) == 0 or (trees_list and len(trees_list) > 0):
            if trees_list:
                GeneticTreeManager.initial_trees = trees_list
            while len(GeneticTreeManager.initial_trees) < number_of_trees:
                new_id = Id.random_connected_id(print_tries=True)
                new_tree = GeneticTree([new_id])
                GeneticTreeManager.initial_trees.append(new_tree)
            GeneticTreeManager.trees = []
            for tree in GeneticTreeManager.initial_trees:
                GeneticTreeManager.trees.append(tree.get_last_child())

    @staticmethod
    def save_tree_list():
        if GeneticTreeManager.results_file_name is None:
            GeneticTreeManager.results_file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        print("Saving results... (Saving frequency: " + str(
            save_results_frequency) + " iterations, filename: " + GeneticTreeManager.results_file_name + ")")
        str_to_write = "[\n\t"
        for i in range(len(GeneticTreeManager.initial_trees)):
            if i > 0:
                str_to_write += ", \n\t"
            str_to_write += GeneticTreeManager.initial_trees[i].to_json()
        str_to_write += "\n]"
        ResultsManager.write_results(GeneticTreeManager.results_file_name, str_to_write)

    @staticmethod
    def print_new_child(old_tree, new_tree, tree_number):
        print(" New child on tree " + str(tree_number) + ": " + str(new_tree.ids[0]) + " (degree=" + str(
            old_tree.degree) + ", diameter=" + str(old_tree.diameter) + ", score1=" + str(
            old_tree.score1) + ") -> (degree=" + str(new_tree.degree) + ", diameter=" + str(
            new_tree.diameter) + ", score1=" + str(new_tree.score1) + ")")

    @staticmethod
    def delete_tree(pos):
        new_connected_id = Id.random_connected_id(print_tries=True)
        new_genetic_tree = GeneticTree([new_connected_id])
        GeneticTreeManager.initial_trees[pos] = new_genetic_tree
        GeneticTreeManager.trees[pos] = new_genetic_tree
        tree = GeneticTreeManager.trees[pos]
        print("  Deleted tree " + str(pos) + " (degree=" + str(tree.degree) + ", diameter=" + str(
            tree.diameter) + ", score1=" + str(tree.score1) + ")")

    @staticmethod
    def delete_all_prepared_to_delete_trees_worst_than(this_tree: GeneticTree):
        for i in range(len(GeneticTreeManager.trees)):
            tree = GeneticTreeManager.trees[i]
            if tree.iterations_without_change >= iterations_without_change_before_preparing_to_delete and \
                    tree.is_score_better_than_self(this_tree.score()):
                GeneticTreeManager.delete_tree(i)

    @staticmethod
    def there_is_prepared_to_delete_tree_better_or_equal_than(this_tree: GeneticTree):
        for i in range(len(GeneticTreeManager.trees)):
            tree = GeneticTreeManager.trees[i]
            if tree.iterations_without_change >= iterations_without_change_before_preparing_to_delete and \
                    tree != this_tree and (this_tree.is_score_better_than_self(tree.score()) or
                                           this_tree.is_score_equal_than_self(tree.score())):
                return True
        return False

    @staticmethod
    def run(iterations: int, number_of_trees: int, trees_list: list = None):

        GeneticTreeManager.__init_trees(number_of_trees, trees_list)

        for i in range(iterations):
            print("Iteration " + str(i) + "/" + str(iterations - 1) + "...")
            sys.stdout.flush()
            for j in range(len(GeneticTreeManager.trees)):
                tree = GeneticTreeManager.trees[j]
                num_ids_prev_to_mutate = len(tree.ids)
                new_tree = tree.mutate()
                num_new_ids = len(new_tree.ids) - num_ids_prev_to_mutate
                if new_tree != tree or num_new_ids > 0:
                    GeneticTreeManager.trees[j] = new_tree
                    if new_tree != tree:
                        GeneticTreeManager.print_new_child(old_tree=tree, new_tree=new_tree, tree_number=j)
                    else:
                        if num_new_ids == 1:
                            print(" New id on tree " + str(j) + ": " + str(tree.ids[0]) + " (num_ids=" +
                                  str(len(tree.ids)) + ", degree=" + str(tree.degree) + ", diameter=" +
                                  str(tree.diameter) + ", score1=" + str(tree.score1) + ")")
                        else:
                            print(" " + str(num_new_ids) + " new ids on tree " + str(j) + " (num_ids=" +
                                  str(len(tree.ids)) + ", degree=" + str(tree.degree) + ", diameter=" +
                                  str(tree.diameter) + ", score1=" + str(tree.score1) + ")")
                    sys.stdout.flush()
                else:
                    print(" Iterations without change on tree " + str(j) + ": " + str(tree.iterations_without_change) +
                          " (num_ids=" + str(len(tree.ids)) + ", degree=" + str(tree.degree) + ", diameter=" +
                          str(tree.diameter) + ", score1=" + str(tree.score1) + ")")
            if (i+1) % save_results_frequency == 0:
                GeneticTreeManager.save_tree_list()
        GeneticTreeManager.save_tree_list()
