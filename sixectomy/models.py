import ast
from collections import namedtuple
import copy
from enum import Enum
import io
import os
import tokenize

import sixectomy.exceptions as sixexcept
from sixectomy.common import python_files
from sixectomy.common import is_pep8_valid

Import = namedtuple("Import", ["module", "name", "alias", "typeof"])
Method = namedtuple("Method", ["node", "name", "docstring"])


class ModuleReader:
    content = None
    encoding = None

    def __init__(self, path):
        self.path = path

    def read(self, force=False):
        if force or not self.content:
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
    name = None
    path = None
    refactored = False
    base = None
    before = None
    # Let's after to none, will be initialized by the surgerer from before
    after = None

    def __init__(self, path):
        """To initalize the analyze class.

        @param path: The path of the file or directory to analyze
        @type path: str
        """
        self.base = {
            'is_pep8_valid': False,
            'tokens': None,
            'tree': None,
            'imports': None,
            'root': None,
        }
        self.before = copy.deepcopy(self.base)
        # Let's after to none, will be initialized by the surgerer from before
        self.after = None
        self.path = path
        self.name = os.path.basename(path)
        self.module_reader = ModuleReader(self.path)
        try:
            self.before['root'] = ast.parse(self.module_reader.read())
        except SyntaxError:
            raise sixexcept.SixectomyException(
                f"Invalid python file {self.name}")
        self.before['imports'] = Imports(self.before['root'])
        self._number_of_six_imports()
        if self.is_using_six():
            # We don't need to tokenize a module that don't use six
            # the goal of sixectomy is to replace six occurences
            # so we can skip to tokenize a module because it's useless
            # in the next of the treatment and we will allocate ressources
            # to something that will not be used.
            # Also checking PEP8 on a module which will be not refactored
            # is useless too, we just want to keep PEP8 compliant a refactored
            # module who was already PEP8 compliant before the refactor.
            # We don't want to spend time on useless things.
            self._tokenizer()
            self.before['is_pep8_valid'] = is_pep8_valid(self.path)

    def prepare_the_refactor(self):
        self.after = copy.deepcopy(self.before)

    def _tokenizer(self):
        bcontent = self.module_reader.bread()
        self.before['tokens'] = [el for el
                                 in tokenize.tokenize(bcontent.readline)]

    def get_tree(self):
        return ast.iter_child_nodes(self.before['root'])

    def is_using_six(self):
        for imp in self.before['imports']:
            if 'six' != imp.name and 'six' != imp.module:
                continue
            return True
        return False

    def _number_of_six_imports(self):
        self.count_import_usages = len(self.before['imports'].get_six())

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
