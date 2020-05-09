import importlib.util
import sys
from os import listdir
from os.path import isfile, join
from commands.Command import Command


def get_available_commands_dict():
    available_commands_dict = {}
    command_folder_files = [f for f in listdir("commands") if isfile(join("commands", f)) and f != "Command.py"]
    for file in command_folder_files:
        spec = importlib.util.spec_from_file_location("", "commands/" + file)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        klass = getattr(foo, file.replace(".py", ""))
        if issubclass(klass, Command):
            available_commands_dict[klass.str_to_execute_command()] = klass
    return available_commands_dict


if __name__ == '__main__':

    commands_dict = get_available_commands_dict()

    if len(sys.argv) <= 1:
        print("")
        print("This script allows the execution of all the functionalities this project provides.")
        print("")
        print("Available commands:")
        for command in commands_dict:
            print(" " + command + " - " + commands_dict[command].description())
        print(" help - Type this command followed by the name of any command above to get more detailed information.")
        print("")
        print("Introduce the command to execute:", end=" ")
        values = input().split(" ")
    else:
        values = sys.argv[1:]

    command = values[0]
    arguments = values[1:] if len(values) > 1 else []

    invalid_command = False

    if command == "help":
        if len(arguments) < 1:
            print("Introduce the command to get more detailed information from:", end=" ")
            command = input()
        else:
            command = arguments[0]
        if command in commands_dict:
            commands_dict[command].print_help()
        else:
            invalid_command = True
    elif command in commands_dict:
        commands_dict[command].execute(arguments)
    else:
        invalid_command = True
    if invalid_command:
        print("Invalid command.")
