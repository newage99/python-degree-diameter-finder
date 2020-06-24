import importlib.util
import sys
import inspect

from os import listdir
from os.path import isfile, join

expression = ''  # Expression to interpret
pos = 0          # Actual position of the expression we are processing
numbers = []     # List of tuples indicating the pairs of numbers pending to be merged
"""
As the interpreter keeps reading the expression, this list gets added functions (single argument functions or
operators) waiting to be computed. When a function computes his input/s, it gets removed from the list.
"""
functions = []


def numbers_count():
    return len(numbers[-1])


def pop_number():
    return numbers[-1].pop()


def push_number(a):
    numbers[-1].append(a)


def get_classes_that_inherit_from(class_they_inherit_from, folder):
    classes = []
    command_folder_files = None
    symbols_folder_locations = [folder, "../" + folder]
    exceptions = ["Symbol.py", "Function.py", "InterpretableSymbol.py", "Number.py", "Operator.py",
                  "SingleArgFunction.py", "Variable.py"]
    for location in symbols_folder_locations:
        try:
            command_folder_files = [f for f in listdir(location) if
                                    isfile(join(location, f)) and f not in exceptions and f.endswith(".py")]
            break
        except Exception as e:
            pass
    symbols_folder_locations = [folder + "/", "./../" + folder + "/"]
    inherit_class = None
    try:
        modules = sys.modules
        test = getattr(modules[folder], class_they_inherit_from)
        members = inspect.getmembers(test)
        for member in members:
            if member[0] == class_they_inherit_from:
                inherit_class = member[1]
                break
    except Exception as e:
        pass
    if inherit_class:
        klass = None
        obj = None
        try:
            for file in command_folder_files:
                foo = None
                for location in symbols_folder_locations:
                    try:
                        spec = importlib.util.spec_from_file_location("", location + file)
                        foo = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(foo)
                        break
                    except Exception as e:
                        pass
                klass = getattr(foo, file.replace(".py", ""))
                obj = klass()
                if issubclass(klass, inherit_class):
                    classes.append(obj)
        except Exception as e:
            pass
    return classes
