import sys

import six


class Compatibility(list):

    def __init__(self):
        self.get_base()
        self.get_moved_modules()
        print(self)

    def get_base(self):
        for el in dir(six):
            if el.startswith("_"):
                continue
            self.append(f'six.{el}')

    def get_moved_modules(self):
        for el in six._importer.known_modules.keys():
            self.append(el)
