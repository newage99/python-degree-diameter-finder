import sys
from commands.Command import Command
from genetic_manager.GeneticTreeManager import GeneticTreeManager


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
        print("Arguments:")
        print("1 - Number of iterations to execute.")
        print("2 [OPTIONAL] - Name of the file to load the list of genetic trees from.")
        print("")
        print("Example: 'python manage.py run 10' will execute 10 iterations of the algorithm.")

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
            if len(sys.argv) > 2:
                pass  # TODO
            GeneticTreeManager.run(iterations)


if __name__ == '__main__':
    RunCommand.execute(sys.argv[1:])
