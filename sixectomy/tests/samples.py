import textwrap

sample = """
import requests
import abc
import six
from six import parse as urlparse
from foo import bar

def baz():
    pass

class Bar:
    def run(self):
        from six.parse import urlencode
        return six.text_type("boom")

    def bar(self):
        urlparse.urlparse("http://test.com/foo/baz")

class Foo:
    pass
"""

samples = [
    textwrap.dedent("""
        import six
        print(six.string_types("baz"))
    """),
    textwrap.dedent("""
        import six import string_types
        print(string_types("baz"))
    """),
]

sample_without_six = """
import requests
import abc
from foo import bar

def baz():
    pass

class Bar:
    def run(self):
        pass

    def bar(self):
        pass

class Foo:
    pass
"""
