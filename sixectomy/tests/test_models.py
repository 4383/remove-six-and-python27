# -*- encoding: utf-8 -*-
import ast
import io
import tempfile
import unittest

import samples

from sixectomy.exceptions import SixectomyException
from sixectomy.models import Analyze
from sixectomy.models import Import
from sixectomy.models import Imports
from sixectomy.models import Module
from sixectomy.models import TypeOfImport
from sixectomy.models import get_functions


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(samples.sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root
        self.functions = get_functions(self.node)

    def test_len(self):
        self.assertEqual(len(self.functions), 1)

    def test_item(self):
        self.assertEqual(self.functions[0].name, "baz")


class TestImports(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(samples.sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root
        self.imports = Imports(self.node)

    def test_init(self):
        self.assertEqual(len(self.imports), 5)

    def test_str(self):
        self.assertEqual(str(self.imports),
                         "requests\nabc\nsix\nparse\nbar")


class TestModules(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(samples.sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root

    def test_parse_file(self):
        self.assertTrue(isinstance(self.node, ast.Module))

    def test_name(self):
        self.assertTrue(self.module.name, self.pyfile.name)

    def test_str(self):
        self.assertTrue(str(self.module), self.pyfile.name)

    def test_get_imports(self):
        imports = self.module.imports
        self.assertEqual(len(imports), 5)
        expected_imports = [
            Import(module=[], name="requests",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module=[], name="abc",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module=[], name="six",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module="six", name="parse",
                   alias='urlparse', typeof=TypeOfImport.FROM),
            Import(module="foo", name="bar",
                   alias=None, typeof=TypeOfImport.FROM),
        ]

        self.assertEqual(imports, expected_imports)

    def test_is_using_six(self):
        self.assertEqual(self.module.is_using_six, True)


class TestModules(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(samples.sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root

    def test_parse_file(self):
        self.assertTrue(isinstance(self.node, ast.Module))

    def test_name(self):
        self.assertTrue(self.module.name, self.pyfile.name)

    def test_str(self):
        self.assertTrue(str(self.module), self.pyfile.name)

    def test_get_imports(self):
        imports = self.module.imports
        self.assertEqual(len(imports), 5)
        expected_imports = [
            Import(module=[], name="requests",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module=[], name="abc",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module=[], name="six",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module="six", name="parse",
                   alias='urlparse', typeof=TypeOfImport.FROM),
            Import(module="foo", name="bar",
                   alias=None, typeof=TypeOfImport.FROM),
        ]

        self.assertEqual(imports, expected_imports)

    def test_is_using_six(self):
        self.assertEqual(self.module.is_using_six(), True)


class TestModulesWithoutSix(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(samples.sample_without_six)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root

    def test_parse_file(self):
        self.assertTrue(isinstance(self.node, ast.Module))

    def test_name(self):
        self.assertTrue(self.module.name, self.pyfile.name)

    def test_str(self):
        self.assertTrue(str(self.module), self.pyfile.name)

    def test_get_imports(self):
        imports = self.module.imports
        self.assertEqual(len(imports), 3)
        expected_imports = [
            Import(module=[], name="requests",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module=[], name="abc",
                   alias=None, typeof=TypeOfImport.DIRECT),
            Import(module="foo", name="bar",
                   alias=None, typeof=TypeOfImport.FROM),
        ]

        self.assertEqual(imports, expected_imports)

    def test_is_using_six(self):
        self.assertEqual(self.module.is_using_six(), False)


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self.fake_files = ["one", "two", "three"]
        self.get_stats_for_single_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            for el in self.fake_files:
                fake = open(
                    "{dir}/{name}.py".format(dir=tmpdir, name=el), "w+"
                )
                fake.write(samples.sample)
            fake = open("{dir}/test.txt".format(dir=tmpdir), "w+")

            self.tmpdir = tmpdir
            self.analyze = Analyze(tmpdir)

    def get_stats_for_single_module(self):
        self.pyfile = io.StringIO(samples.sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root
        self.imports_number = len(self.module.imports)

    def get_expected_modules_len(self):
        return len(self.fake_files)

    def get_expected_total_imports(self):
        return self.get_expected_modules_len() * self.imports_number

    def test_modules(self):
        self.assertEqual(
            len(self.analyze.modules), self.get_expected_modules_len()
        )

    def test_module_imports(self):
        self.assertEqual(
            len(self.analyze.modules[0].imports), self.imports_number
        )

    def test_count_total_modules_using_six(self):
        # here all the given fake python modules using six
        # so we have as many modules as modules using six
        self.assertEqual(
            self.get_expected_modules_len(), self.analyze.modules_using_six
        )

    def test_modules_total_imports(self):
        self.assertEqual(
            self.analyze.imports, self.get_expected_total_imports()
        )

    def test_analyze_on_single_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)
            with open(module_path, "w+") as module:
                module.write(samples.sample)

            sh_path = "{dir}/script.sh".format(dir=tmpdir)
            with open(sh_path, "w+") as sh:
                sh.write("echo test!")

            self.analyze = Analyze(module_path)

            with self.assertRaises(SixectomyException):
                self.analyze = Analyze(sh_path)

            try:
                fake = "{dir}/fake".format(dir=tmpdir)
                self.analyze = Analyze(fake)
            except SixectomyException as err:
                self.assertEqual(
                    str(err), "Path not found: {fake}".format(fake=fake)
                )
