import json
import sys
from commands.Command import Command
from genetic_manager.GeneticTreeManager import GeneticTreeManager
from genetic_manager.GeneticTree import GeneticTree
from topology_manager.ResultsManager import ResultsManager
from misc.config import number_of_trees


class RunCommand(Command):

    @staticmethod
    def str_to_execute_command():
        return "run"

    @staticmethod
    def description():
        return "Executes the genetic algorithm for a given number of iterations."

    @staticmethod
    def print_help():
        print("")
        print("'run' command executes the genetic algorithm for an specified number of iterations.")
        # TODO: Print here a more detailed explanation about what the genetic algorithm is about.
        print("")
        print("MANDATORY ARGUMENTS:")
        print("Position 1 -> Number of iterations to execute.")
        print("")
        print("OPTIONAL ARGUMENTS:")
        print("--load=<file_name> ->          If you type '--load=' and then you specify a file name existing on " +
              "results folder, the tree list contained in that file is going to be loaded and used to execute the " +
              "genetic algorithm.")
        print("--save=<file_name> ->          If you type '--save=' and then specify a file name, the results of the " +
              "genetic algorithm execution are going to be saved with that file name on results folder.")
        print("                               If you don't specify any --save argument, results file name is going " +
              "to be preserved from --load file name or if --load argument was not specified, is going to be formed " +
              "by the timestamp at the moment of saving.")
        print("--ntrees=<number_of_trees> ->  If you type '--ntrees' and then you specify a positive integer, this " +
              "will set the number of trees the list has.")
        print("")
        print("EXAMPLES:")
        print(" 'python manage.py run 10'                             will execute 10 iterations of the algorithm. " +
              "Results file name will be the timestamp at the moment of saving.")
        print(" 'python manage.py run 22 --load=2020_05_10_16_34_37'  will execute 22 iterations of the algorithm on " +
              "existing tree list stored in file '2020_05_10_16_34_37.json'. Results will be stored on the same file.")
        print(" 'python manage.py run 37 --load=test1 --save=test2'   will execute 37 iterations on tree list stored " +
              "in 'test1.json' file, but results will be stored on file 'test2.json'.")
        print(" 'python manage.py run 120 --ntrees=5'                 will execute 120 iterations of the algorithm " +
              "using a list of 5 trees.")

    @staticmethod
    def retrieve_iterations(arguments):
        if len(arguments) < 1:
            print('Introduce the number of operations you want to perform:', end=" ")
            iterations_str = input()
        else:
            iterations_str = arguments[0]
        try:
            iterations = int(iterations_str)
        except Exception as e:
            iterations = -1
        if iterations <= 0:
            print('Number of iterations must be a positive integer.')
        return iterations

    @staticmethod
    def load_tree_list(i, values):
        trees_list = []
        invalid_argument_pos_and_reason = None
        if len(values) < 2 or len(values[1]) <= 0:
            invalid_argument_pos_and_reason = [i, "Load file name not provided."]
        else:
            results_file, error_reason = ResultsManager.read_results(values[1])
            if error_reason:
                invalid_argument_pos_and_reason = [i, error_reason]
            else:
                GeneticTreeManager.results_file_name = values[1]
                try:
                    trees_dict_list = json.loads(results_file)
                    for tree_dict in trees_dict_list:
                        trees_list.append(GeneticTree.from_dict(tree_dict))
                except Exception as e:
                    invalid_argument_pos_and_reason = [i, "Error parsing results json: " + str(e)]
        return trees_list, invalid_argument_pos_and_reason

    @staticmethod
    def retrieve_number_of_trees(i, values):
        n_trees = number_of_trees
        invalid_argument_pos_and_reason = None
        if len(values) < 2 or len(values[1]) <= 0:
            invalid_argument_pos_and_reason = [i, "Number of trees not provided"]
        else:
            try:
                n_trees = int(values[1])
                if n_trees <= 0:
                    invalid_argument_pos_and_reason = [i, "Number of trees is not a positive integer"]
            except Exception as e:
                invalid_argument_pos_and_reason = [i, "Number of trees is not an integer"]
        return n_trees, invalid_argument_pos_and_reason

    @staticmethod
    def execute(arguments):
        iterations = RunCommand.retrieve_iterations(arguments)
        if iterations > 0:
            trees_list = []
            invalid_argument_pos_and_reason = None
            n_trees = number_of_trees
            if len(arguments) > 1:
                for i in range(1, len(arguments)):
                    arg = arguments[i]
                    if arg.startswith('--load='):
                        trees_list, invalid_argument_pos_and_reason = RunCommand.load_tree_list(i, arg.split("="))
                    elif arg.startswith('--save='):
                        values = arg.split("=")
                        if len(values) < 2 or len(values[1]) <= 0:
                            invalid_argument_pos_and_reason = [i, "Read file name not provided"]
                        else:
                            GeneticTreeManager.results_file_name = values[1]
                    elif arg.startswith('--ntrees='):
                        n_trees = RunCommand.retrieve_number_of_trees(i, arg.split("="))
                    else:
                        invalid_argument_pos_and_reason = [i, "Argument not recognized."]
                    if invalid_argument_pos_and_reason:
                        break
            if invalid_argument_pos_and_reason:
                pos = invalid_argument_pos_and_reason[0]
                reason = invalid_argument_pos_and_reason[1]
                print("Error at argument in position " + str(pos) + ": " + reason)
            else:
                GeneticTreeManager.run(iterations, n_trees, trees_list)


if __name__ == '__main__':
    RunCommand.execute(sys.argv[1:])
