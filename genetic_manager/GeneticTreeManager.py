import os
import json
from datetime import datetime
from misc.config import number_of_trees
from misc.config import save_results_frequency
from genetic_manager.GeneticTree import GeneticTree
from topology_manager.IdGenerator import IdGenerator


class GeneticTreeManager:

    initial_trees = []
    trees = []
    number_of_iterations = 0
    winning_tree = None
    iterations_when_last_saved = 0
    results_file_name = "this_string_should_not_appear_as_txt_name"

    @staticmethod
    def get_project_dir():
        project_dir = os.path.dirname(__file__)
        # This next line makes direct debug run from RunCommand work
        project_dir = project_dir.replace("\\genetic_manager", "") if "genetic_manager" in project_dir else project_dir
        return project_dir

    @staticmethod
    def create_results_folder_if_does_not_exists():
        if not os.path.exists("results"):
            os.makedirs("results")

    @staticmethod
    def save_results():
        GeneticTreeManager.iterations_when_last_saved = GeneticTreeManager.number_of_iterations
        initial_trees = GeneticTreeManager.initial_trees
        str_to_write = "[\n\t"
        for i in range(len(initial_trees)):
            if i > 0:
                str_to_write += ", \n\t"
            str_to_write += initial_trees[i].to_json()
        str_to_write += "\n]"
        GeneticTreeManager.create_results_folder_if_does_not_exists()
        full_file_name = GeneticTreeManager.results_file_name + ".txt"
        filename = os.path.join(GeneticTreeManager.get_project_dir(), "results\\" + full_file_name)
        f = open(filename, "w+")
        f.write(str_to_write.replace("'", '"'))
        f.close()

    @staticmethod
    def run(iterations):
        trees = GeneticTreeManager.trees
        initial_trees = GeneticTreeManager.initial_trees
        if len(initial_trees) == 0:
            while len(initial_trees) < number_of_trees:
                new_tree = GeneticTree(IdGenerator.generate_connected_matrix_id())
                initial_trees.append(new_tree)
                trees.append(new_tree)
            GeneticTreeManager.results_file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        final_number_of_iterations = GeneticTreeManager.number_of_iterations + iterations

        for i in range(GeneticTreeManager.number_of_iterations, final_number_of_iterations):
            print("Iteration " + str(i + 1) + "/" + str(final_number_of_iterations) + "...")
            for j in range(len(trees)):
                new_tree = trees[j].mutate()
                if new_tree != trees[j]:
                    print("Tree " + str(j) + ":  " + trees[j].id + "  (degree=" + str(
                        trees[j].degree) + ", diameter=" + str(trees[j].diameter) + ", score1=" + str(
                        trees[j].score1) + ") mutated to  " + new_tree.id + "  (degree=" + str(
                        new_tree.degree) + ", diameter=" + str(new_tree.diameter) + ", score1=" + str(
                        new_tree.score1) + ")")
                    trees[j] = new_tree
            if i > 0 and i % save_results_frequency == 0:
                GeneticTreeManager.save_results()
            GeneticTreeManager.number_of_iterations += 1
        if GeneticTreeManager.iterations_when_last_saved != final_number_of_iterations:
            GeneticTreeManager.save_results()

