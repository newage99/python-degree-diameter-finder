from commands.Command import Command


class RunCommand(Command):

    def str_to_execute_command(self):
        return "run"

    def help(self):
        print("The command 'run' executes the genetic algorithm for an specified number of iterations.")
        print("The number of iterations must be provided as the first argument of the script.")
        print("Example: 'python manage.py run 10' will execute 10 iterations of the algorithm.")

    def execute(self):
        pass
