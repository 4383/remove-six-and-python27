import ast
from collections import namedtuple
from enum import Enum
import io
import os
import tokenize

import sixectomy.exceptions as sixexcept
from sixectomy.common import python_files

Import = namedtuple("Import", ["module", "name", "alias", "typeof"])
Method = namedtuple("Method", ["node", "name", "docstring"])


class ModuleReader:
    content = None
    encoding = None

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as content:
            self.content = content.read()
            return self.content

    def bread(self):
        if not self.content:
            self.read()
        return io.BytesIO(self.content.encode('utf-8'))


class TypeOfImport(Enum):
    DIRECT=1,
    FROM=2


def is_six_import(imp):
    if isinstance(imp.module, list):
        return 'six' == imp.name
    return 'six' == imp.name or \
           'six' == imp.module or \
           imp.module.startswith('six.')


def parse_import(node):
    if isinstance(node, ast.Import):
        return [], TypeOfImport.DIRECT
    elif isinstance(node, ast.ImportFrom):
        return node.module, TypeOfImport.FROM
    else:
        raise sixexcept.SixectomyImportException(f"Not an import ({node})")


class Imports(list):
    def __init__(self, root):
        """Initialize list of imports."""
        super(Imports, self).__init__()
        for node in ast.iter_child_nodes(root):
            try:
                module, typeof = parse_import(node)
            except sixexcept.SixectomyImportException:
                continue
            else:
                for name in node.names:
                    self.append(Import(module, name.name, name.asname, typeof))

    def get_six(self):
        return [imp for imp in self if is_six_import(imp)]


class Module:
    count_import_usages = 0
    root = None
    name = None
    path = None
    tokens = None

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.path = path
        self.name = os.path.basename(path)
        self.module_reader = ModuleReader(self.path)
        try:
            self.root = ast.parse(self.module_reader.read())
        except SyntaxError:
            raise sixexcept.SixectomyException(
                f"Invalid python file {self.name}")
        self.imports = Imports(self.root)
        self._number_of_six_imports()
        if self.is_using_six():
            self.tokenizer()

    def tokenizer(self):
        bcontent = self.module_reader.bread()
        self.tokens = tokenize.tokenize(bcontent.readline)

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
            self.modules.append(Module(self.path))
        elif os.path.isdir(self.path):
            for module in python_files(self.path):
                self.modules.append(Module(module))
        else:
            raise sixexcept.SixectomyException(f"Path not found: {path}")
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
