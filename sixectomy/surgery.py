import abc
import ast

from sixectomy.exceptions import SixectomyException


class SurgererTools(metaclass=abc.ABCMeta):

    def __new__(cls, node):
        type_of = type(node).__name__.lower().replace('def', '')

        for sub in cls.__subclasses__():
            if sub.isDesignedFor(type_of):
                o = object.__new__(sub)
                o.__init__(type_of)
                return o

        raise SixectomyException(f"No available tools found for {node}")

    def __init__(self, node):
        self.node = node

    @classmethod
    def isDesignedFor(cls, type_of):
        if type_of == cls.__name__.lower().replace("surgerertools", ""):
            return cls
        return False

    @abc.abstractmethod
    def act(self):
        raise NotImplemented

    @abc.abstractmethod
    def examine(self):
        raise NotImplemented


class FunctionSurgererTools(SurgererTools):

    def act(self):
        print('acting on function')

    def examine(self):
        print(f'function examine {self.node}')


class ClassSurgererTools(SurgererTools):

    def act(self):
        print('acting on class')

    def examine(self):
        print(f'class examine {self.node}')


class AssignSurgererTools(SurgererTools):

    def act(self):
        print('acting on class')

    def examine(self):
        print(f'expr examine {self.node}')
        print(self.node.lineno)
        print(self.node.value)
        print(dir(self.node))


class ExprSurgererTools(SurgererTools):

    def act(self):
        print('acting on class')

    def examine(self):
        print(f'expr examine {self.node}')
        print(self.node.lineno)
        print(self.node.value)
        print(dir(self.node))


class Operating:

    def __init__(self, analyze):
        self.analyze = analyze

    def act(self):
        for module in self.analyze.modules:
            if not module.is_using_six():
                continue

            surgerer = Surgerer(module)
            surgerer.surgery()

class Surgerer:

    def __init__(self, module):
        self.module = module

    def surgery(self):
        for node in self.module.tree():
            try:
                tools = SurgererTools(node)
                tools.examine()
            except SixectomyException as ex:
                print(ex)
                continue

