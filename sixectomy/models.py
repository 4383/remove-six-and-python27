import ast
from enum import Enum
import os
from collections import namedtuple

from sixectomy.common import python_files
from sixectomy.exceptions import SixectomyException

Import = namedtuple("Import", ["module", "name", "alias", "typeof"])
Method = namedtuple("Method", ["node", "name", "docstring"])


class TypeOfImport(Enum):
    DIRECT=1,
    FROM=2


def get_functions(root):
    funcs = []
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.FunctionDef):
            funcs.append(Method(node, node.name, ast.get_docstring(node)))
    return funcs


def is_six_import(imp):
    if isinstance(imp.module, list):
        return 'six' == imp.name
    return 'six' == imp.name or \
           'six' == imp.module or \
           imp.module.startswith('six.')


class Imports(list):
    def __init__(self, root):
        """Initialize list of imports."""
        super(Imports, self).__init__()
        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                module = []
                typeof = TypeOfImport.DIRECT
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                typeof = TypeOfImport.FROM
            else:
                continue

            for name in node.names:
                self.append(Import(module, name.name, name.asname, typeof))

    def get_six(self):
        return [imp for imp in self if is_six_import(imp)]


class Module:
    count_import_usages = 0

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.name = path.name
        try:
            self.root = ast.parse(self.path.read())
        except SyntaxError:
            raise SixectomyException(
                "Invalid python file {filename}".format(filename=self.name)
            )
        self.imports = Imports(self.root)
        self._number_of_six_imports()

    def tree(self):
        return ast.iter_child_nodes(self.root)

    def is_using_six(self):
        for imp in self.imports:
            if 'six' != imp.name and 'six' != imp.module:
                continue
            return True
        return False

    def _number_of_six_imports(self):
        self.count_import_usages = len(self.imports.get_six())

    def __str__(self):
        """Textual representation of module."""
        return self.name


class Analyze(object):
    """To analyze the file."""

    path = None
    modules = []
    number_of_total_modules = 0
    number_of_usages = 0

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.modules = []
        if os.path.isfile(self.path):
            with open(self.path, "r") as pyfile:
                self.modules.append(Module(pyfile))
        elif os.path.isdir(self.path):
            for module in python_files(self.path):
                with open(module, "r") as pyfile:
                    current_module = Module(pyfile)
                    self.modules.append(current_module)
        else:
            raise SixectomyException(
                "Path not found: {path}".format(path=path)
            )
        self._count_six_usages()
        self._count_number_of_total_modules()

    def is_positive(self):
        """
        Do the analyze is positive?
        Do we found six occurences during analyze?
        """
        return self.number_of_usages > 0

    def _count_number_of_total_modules(self):
        self.number_of_total_modules = len(self.modules)

    def _count_six_usages(self):
        """
        How many modules in the analyze using six?
        """
        for module in self.modules:
            self.number_of_usages += 1 if module.is_using_six() else 0
