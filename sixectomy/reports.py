import abc

from sixectomy.exceptions import SixectomyException


class Report(metaclass=abc.ABCMeta):
    def __new__(cls, analyze, report_type='simple'):
        if not analyze.is_positive():
            o = object.__new__(EmptyReport)
            o.__init__(analyze)
            return o

        for sub in cls.__subclasses__():
            if sub.isDesignedFor(report_type):
                o = object.__new__(sub)
                o.__init__(analyze)
                return o

        raise SixectomyException(f"Not report corresponding to {report_type}")

    def __init__(self, analyze, report_type='simple'):
        self.analyze = analyze

    @abc.abstractmethod
    def rendering(self):
        return NotImplemented

    @classmethod
    def isDesignedFor(cls, report_type):
        if report_type == cls.__name__.lower().replace("report", ""):
            return cls
        return False


class SimpleReport(Report):

    def rendering(self):
        print('This project using six!')
        print(f'Number of analyzed files: '
              f'{self.analyze.number_of_total_modules}')
        print(f'Number of modules using six: {self.analyze.number_of_usages}')
        print('')
        print('List of modules using six:')
        print('\n'.join([f'{mod}: imports: {mod.count_import_usages}' \
                         for mod in self.analyze.modules \
                         if mod.is_using_six()]))


class AdvancedReport(Report):

    def rendering(self):
        print(f'No six usages founds in ')

class EmptyReport(Report):

    def rendering(self):
        print(f'No six usages founds in {self.analyze.path}')
