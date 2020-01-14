import ast
import io
import os
import tempfile
import types
import unittest

import samples

import sixectomy.exceptions as sixexcept
from sixectomy.models import parse_import
from sixectomy.models import Analyze
from sixectomy.models import Import
from sixectomy.models import Imports
from sixectomy.models import Module
from sixectomy.models import ModuleReader
from sixectomy.models import TypeOfImport


class TestModuleReader(unittest.TestCase):
    def setUp(self):
        self.pyfile = "test.txt"
        with tempfile.TemporaryDirectory() as tmpdir:
            fake = open(os.path.join(tmpdir, self.pyfile), "w+")
            fake.write(samples.codes.with_six)
            fake.close()
            self.tmpdir = tmpdir
            self.file_to_handle = os.path.join(self.tmpdir, self.pyfile)
            self.mr = ModuleReader(self.file_to_handle)
            self.content = self.mr.read()
            self.bcontent = self.mr.bread()

    def test_init(self):
        self.assertTrue(isinstance(self.mr, ModuleReader))

    def test_read(self):
        self.assertTrue(isinstance(self.content, str))

    def test_bread(self):
        self.assertTrue(isinstance(self.bcontent, io.BytesIO))
        self.assertTrue(isinstance(
            self.bcontent,
            type(io.BytesIO(self.content.encode('utf-8')))))

    def test_bread_call_read(self):
        backup = self.content
        self.mr.content = None
        self.content = None
        with tempfile.TemporaryDirectory() as tmpdir:
            fake = open(os.path.join(tmpdir, self.pyfile), "w+")
            fake.write(samples.codes.with_six)
            fake.close()
            self.mr = ModuleReader(os.path.join(tmpdir, self.pyfile))
            self.bcontent = self.mr.bread()
            self.content = self.mr.content
        self.assertTrue(isinstance(self.bcontent, io.BytesIO))
        self.assertTrue(self.content is not None)
        self.assertEqual(self.mr.content, backup)
        self.assertTrue(isinstance(
            self.bcontent,
            type(io.BytesIO(self.content.encode('utf-8')))))


class TestImports(unittest.TestCase):
    def setUp(self):
        self.pyfile = "test.txt"
        with tempfile.TemporaryDirectory() as tmpdir:
            fake = open(os.path.join(tmpdir, self.pyfile), "w+")
            fake.write(samples.codes.with_six)
            fake.close()
            self.tmpdir = tmpdir
            self.module = Module(os.path.join(self.tmpdir, "test.txt"))
            self.node = self.module.root
            self.imports = Imports(self.node)

    def test_parse_import(self):
        # Test a node as an import
        node = ast.Import("blabla")
        module, typeof = parse_import(node)
        self.assertEqual(module, [])
        self.assertEqual(typeof, TypeOfImport.DIRECT)
        # Test a node as not an import
        node = ast.Delete("blabla")
        with self.assertRaises(sixexcept.SixectomyImportException):
            parse_import(node)

    def test_init(self):
        self.assertEqual(len(self.imports), 5)
        self.assertEqual(self.imports, samples.imports.with_six)

    def test_get_six(self):
        self.assertEqual(len(self.imports.get_six()), 2)


class TestModules(unittest.TestCase):
    def setUp(self):
        self.pyfile = "test.txt"
        with tempfile.TemporaryDirectory() as tmpdir:
            fake = open(os.path.join(tmpdir, self.pyfile), "w+")
            fake.write(samples.codes.with_six)
            fake.close()
            self.tmpdir = tmpdir
            self.module = Module(os.path.join(self.tmpdir, "test.txt"))

    def test_parse_file(self):
        self.assertTrue(isinstance(self.module.root, ast.Module))

    def test_name(self):
        self.assertTrue(self.module.name, self.pyfile)

    def test_str(self):
        self.assertTrue(str(self.module), self.pyfile)

    def test_get_imports(self):
        imports = self.module.imports
        self.assertEqual(len(imports), 5)
        self.assertEqual(imports, samples.imports.with_six)

    def test_is_using_six(self):
        self.assertEqual(self.module.is_using_six(), True)

    def test_tokenizer(self):
        self.assertTrue(isinstance(self.module.before, types.GeneratorType))
        content = [str(el) for el in self.module.before]
        for el in content:
            self.assertTrue('TokenInfo' in el)


class TestModulesWithoutSix(unittest.TestCase):
    def setUp(self):
        self.pyfile = "test.txt"
        with tempfile.TemporaryDirectory() as tmpdir:
            fake = open(os.path.join(tmpdir, self.pyfile), "w+")
            fake.write(samples.codes.without_six)
            fake.close()
            self.tmpdir = tmpdir
            self.module = Module(os.path.join(self.tmpdir, "test.txt"))
            self.node = self.module.root

    def test_parse_file(self):
        self.assertTrue(isinstance(self.node, ast.Module))

    def test_name(self):
        self.assertTrue(self.module.name, self.pyfile)

    def test_str(self):
        self.assertTrue(str(self.module), self.pyfile)

    def test_get_imports(self):
        imports = self.module.imports
        self.assertEqual(len(imports), 3)
        self.assertEqual(imports, samples.imports.without_six)

    def test_is_using_six(self):
        self.assertEqual(self.module.is_using_six(), False)

    def test_tokenizer(self):
        self.assertTrue(self.module.before is None)


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self.fake_files = ["one", "two", "three"]
        self.get_stats_for_single_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            for el in self.fake_files:
                fake = open(
                    "{dir}/{name}.py".format(dir=tmpdir, name=el), "w+"
                )
                fake.write(samples.codes.with_six)
                fake.close()
            fake = open("{dir}/test.txt".format(dir=tmpdir), "w+")
            fake.close()

            self.tmpdir = tmpdir
            self.analyze = Analyze(tmpdir)

    def get_stats_for_single_module(self):
        self.pyfile = "test.txt"
        with tempfile.TemporaryDirectory() as tmpdir:
            fake = open(os.path.join(tmpdir, self.pyfile), "w+")
            fake.write(samples.codes.with_six)
            fake.close()
            self.tmpdir = tmpdir
            self.module = Module(os.path.join(self.tmpdir, "test.txt"))
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

    def test_count_total_number_of_usages(self):
        # here all the given fake python modules using six
        # so we have as many modules as modules using six
        self.assertEqual(
            self.get_expected_modules_len(), self.analyze.number_of_usages
        )

    def test_analyze_on_single_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)
            with open(module_path, "w+") as module:
                module.write(samples.codes.with_six)

            sh_path = "{dir}/script.sh".format(dir=tmpdir)
            with open(sh_path, "w+") as sh:
                sh.write("echo test!")

            self.analyze = Analyze(module_path)

            with self.assertRaises(sixexcept.SixectomyException):
                self.analyze = Analyze(sh_path)

            try:
                fake = "{dir}/fake".format(dir=tmpdir)
                self.analyze = Analyze(fake)
            except sixexcept.SixectomyException as err:
                self.assertEqual(
                    str(err), "Path not found: {fake}".format(fake=fake)
                )
