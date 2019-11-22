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
