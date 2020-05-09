import sys
from commands.Command import Command
from genetic_manager.GeneticTreeManager import GeneticTreeManager


class RunCommand(Command):

    @staticmethod
    def str_to_execute_command():
        return "run"

    @staticmethod
    def help():
        print("This command executes the genetic algorithm for an specified number of iterations.")
        print("Arguments:")
        print("1 - Number of iterations to execute.")
        print("2 [OPTIONAL] - Name of the file to load the list of genetic trees from.")
        print("Example: 'python manage.py run 10' will execute 10 iterations of the algorithm.")

    @staticmethod
    def execute():
        if len(sys.argv) < 2:
            print('Introduce the number of operations you want to perform:', end=" ")
            iterations = input()
        else:
            iterations = sys.argv[1]
        invalid_iterations = False
        try:
            iterations = int(iterations)
            if iterations <= 0:
                invalid_iterations = True
        except Exception as e:
            invalid_iterations = True
        if invalid_iterations:
            print('Number of iterations must be a positive integer.')
        else:
            trees_list = []
            if len(sys.argv) > 2:
                pass
            GeneticTreeManager.run(iterations)


if __name__ == '__main__':
    RunCommand.execute()
