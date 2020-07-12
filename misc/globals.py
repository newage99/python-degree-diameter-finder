import importlib.util
import sys
import inspect

from os import listdir
from os.path import isfile, join, isdir, dirname, abspath

expression = ''  # Expression to interpret
pos = 0          # Actual position of the expression we are processing
numbers = []     # List of tuples indicating the pairs of constants pending to be merged
"""
As the interpreter keeps reading the expression, this list gets added functions (single argument functions or
operators) waiting to be computed. When a function computes his input/s, it gets removed from the list.
"""
functions = []
slash = "\\" if sys.platform == "win32" else "/"


def numbers_count():
    return len(numbers[-1])


def pop_number():
    return numbers[-1].pop()


def push_number(a):
    numbers[-1].append(a)


def get_relative_path(abs_path: str):
    folders = abs_path.split(slash)
    pos_of_root = folders.index("python-degree-diameter-finder")
    folders = folders[pos_of_root + 1:]
    return slash.join(folders)


def __get_class(klass: str, folder: str):
    try:
        modules = sys.modules
        folders = folder.split(slash)
        module = modules[folders[0]]
        for i in range(1, len(folders)):
            module = getattr(module, folders[i])
        file = getattr(module, klass)
        members = inspect.getmembers(file)
        for member in members:
            if member[0] == klass:
                return member[1]
    except Exception as e:
        pass
    return None


def __recursively_get_files(folder: str, exceptions: list):
    files = []
    for f in listdir(folder):
        path = join(folder, f)
        if isdir(path):
            files = files + __recursively_get_files(join(folder, f), exceptions)
        elif isfile(path) and f.endswith(".py") and f not in exceptions:
            files.append(path)
    return files


def get_class_name_that_implemented_function(func):
    return func.__globals__['__name__'].split(".")[-1]


def get_symbol_classes_that_inherit_from(class_they_inherit_from, function_they_implement_name: str):

    a = inspect.stack()[1]
    b = a[1]
    c = abspath(b)
    d = dirname(c)
    folder = get_relative_path(d)
    classes = {}
    inherit_class = __get_class(class_they_inherit_from, folder)

    if inherit_class:

        symbols_folder_locations = [folder, ".." + slash + folder]
        location = None
        for possible_location in symbols_folder_locations:
            if isdir(possible_location):
                location = possible_location
                break
        if location:
            exceptions = ["Symbol.py", "Function.py", "InterpretableSymbol.py", "Operator.py",
                          "SingleArgFunction.py", "Constant.py", "Number.py", "Variable.py"]
            paths = __recursively_get_files(location, exceptions)
            symbols_folder_locations = ["", "." + slash + ".." + slash]
            klass = None
            obj = None
            try:
                for path in paths:
                    foo = None
                    for location in symbols_folder_locations:
                        try:
                            spec = importlib.util.spec_from_file_location("", location + path)
                            foo = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(foo)
                            break
                        except Exception as e:
                            pass
                    path_split = path.split(slash)
                    klass = getattr(foo, str(path_split[-1]).replace(".py", ""))
                    if issubclass(klass, inherit_class):
                        obj = klass()
                        if callable(getattr(obj, function_they_implement_name, None)):
                            class_str = str(obj)
                            if class_str in classes:
                                classes[class_str].append(obj)
                            else:
                                classes[class_str] = [obj]
            except Exception as e:
                pass
    return classes
