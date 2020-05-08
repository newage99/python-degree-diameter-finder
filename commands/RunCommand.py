import sys
from commands.Command import Command
from genetic_manager.GeneticTreeManager import GeneticTreeManager


class RunCommand(Command):

    def str_to_execute_command(self):
        return "run"

    def help(self):
        print("The command 'run' executes the genetic algorithm for an specified number of iterations.")
        print("The number of iterations must be provided as the first argument of the script.")
        print("Example: 'python manage.py run 10' will execute 10 iterations of the algorithm.")

    def execute(self):
        if len(sys.argv) < 2:
            print('Introduce the number of operations you want to perform: ', end=" ")
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
            GeneticTreeManager.run(iterations)
