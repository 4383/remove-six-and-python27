import textwrap


with_six = """
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

without_six = """
import requests
import abc
from foo import bar
from baz import buz, boom, beh
from baz import biz as bazbiz

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
