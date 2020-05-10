import json
import sys
from commands.Command import Command
from genetic_manager.GeneticTreeManager import GeneticTreeManager
from genetic_manager.GeneticTree import GeneticTree
from misc.ResultsManager import ResultsManager


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
        print("--load=<file_name> -> If you type '--load=' and then you specify a file name existing on results " +
              "folder, the tree list contained in that file is going to be loaded and used to execute the genetic " +
              "algorithm.")
        print("--save=<file_name> -> If you type '--save=' and then specify a file name, the results of the genetic " +
              "algorithm execution are going to be saved with that file name on results folder.")
        print("If you don't specify any --save argument, results file name is going to be preserved from --load " +
              "file name or if --load argument was not specified, is going to be formed by the timestamp at the " +
              "moment of saving.")
        print("")
        print("EXAMPLES:")
        print(" 'python manage.py run 10'                             will execute 10 iterations of the algorithm. " +
              "Results file name will be the timestamp at the moment of saving.")
        print(" 'python manage.py run 22 --load=2020_05_10_16_34_37'  will execute 22 iterations of the algorithm on " +
              "existing tree list stored in file '2020_05_10_16_34_37.json'. Results will be stored on the same file.")
        print(" 'python manage.py run 37 --load=test1 --save=test2'   will execute 37 iterations on tree list stored " +
              "in 'test1.json' file, but results will be stored on file 'test2.json'.")

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
    def execute(arguments):
        iterations = RunCommand.retrieve_iterations(arguments)
        if iterations > 0:
            trees_list = []
            invalid_argument_pos_and_reason = None
            if len(arguments) > 1:
                save_file_name = None
                for i in range(1, len(arguments)):
                    arg = arguments[i]
                    if arg.startswith('--load='):
                        values = arg.split("=")
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
                    elif arg.startswith('--save='):
                        values = arg.split("=")
                        if len(values) < 2 or len(values[1]) <= 0:
                            invalid_argument_pos_and_reason = [i, "Read file name not provided"]
                        else:
                            save_file_name = values[1]
                    else:
                        invalid_argument_pos_and_reason = [i, "Argument not recognized."]
                    if invalid_argument_pos_and_reason:
                        break
                if save_file_name:
                    GeneticTreeManager.results_file_name = save_file_name
            if invalid_argument_pos_and_reason:
                pos = invalid_argument_pos_and_reason[0]
                reason = invalid_argument_pos_and_reason[1]
                print("Error at argument in position " + str(pos) + ": " + reason)
            else:
                GeneticTreeManager.run(iterations, trees_list)


if __name__ == '__main__':
    RunCommand.execute(sys.argv[1:])