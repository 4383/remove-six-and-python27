import unittest

from sixectomy.compatibility import Compatibility


class TestCompatibility(unittest.TestCase):
    def setUp(self):
        self.compat = Compatibility()

    def test_init(self):
        self.assertTrue(isinstance(self.compat, list))
