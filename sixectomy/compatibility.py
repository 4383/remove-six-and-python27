import re
import sys

import six

from sixectomy.exceptions import SixectomyCompatibilityException


def parse_line(line):
    # To more merely understand the following regex
    # please take a look to https://regex101.com/r/yPiWr3/1
    search = r'Moved\w+([\("_a-zA-Z,\s.+\(\)<=>1-9]*),'
    match = re.match(search, line)
    # order is important match can be equal to None so he need
    # to be tested first to exit the and condition if is None
    # if match is None the groups attribut doesn't exist and it will raise
    # an exception
    if match and match.groups():
        return match.group(1)
    raise SixectomyCompatibilityException(
        f"No pattern match with line ({line})")


class Compatibility(list):

    _ignored = ['Module_six', 'MovedAttribute', 'MovedModule']
    _sources = []
    _mapping = []

    def __init__(self):
        self._get_base()
        self._get_moved_modules()
        self._get_specific_submodules()
        self._read_six_sources()
        self._set_mapping()

    def _read_six_sources(self):
        with open(six.__file__) as sixfile:
            for line in sixfile.readlines():
                line = line.strip()
                if not line.startswith("MovedModule(") and \
                   not line.startswith("MovedAttribute("):
                    continue
                self._sources.append(line)


    def _get_base(self):
        for el in dir(six):
            if el.startswith("_") or \
               True in (True for ign in self._ignored if el.startswith(ign)):
                continue
            self.append(f'six.{el}')

    def _get_moved_modules(self):
        for el in six._importer.known_modules.keys():
            if el not in self:
                self.append(el)

    def _get_specific_submodules(self):
        for attribut in dir(six):
            if not attribut.startswith('Module_six'):
                continue
            for el in dir(getattr(six, attribut)):
                if not el.startswith("_"):
                    module_name = attribut.split("_")[1:]
                    new_module = "{path}.{name}".format(
                        path=".".join(module_name), name=el)
                    if new_module not in self:
                        self.append(new_module)
                    new_module = "{pre}.{post}.{name}".format(
                        pre=".".join(module_name[0:2]),
                        post="_".join(module_name[2:]), name=el)
                    if new_module not in self:
                        self.append(new_module)

    def _need_mapping(self, name, line):
        return f"MovedModule('{name}'" in line or \
           f'MovedModule("{name}"' in line or \
           f"MovedAttribute('{name}'" in line or \
           f'MovedAttribute("{name}"' in line

    def get_py3_module_mapping(self, line):
        line = line.replace("\n", "")
        if line[-1] == ",":
            line = line[0:-1]
        return line.split(",")[-1].replace(")", "").replace(
            '"', "").replace("'", "").replace(",", "").strip()

    def _set_mapping(self):
        for line in self._sources:
            for el in self:
                module = el.split(".")
                if self._need_mapping(module[-1], line):
                    if "MovedAttribute" in line:
                        py3 = "{path}.{module}".format(
                              path=self.get_py3_module_mapping(line),
                              module=module[-1])
                    else:
                        py3 = self.get_py3_module_mapping(line)
                    maps = {
                        "six": ".".join(module),
                        "py3": py3
                    }
                    if maps not in self._mapping:
                        self._mapping.append(maps)
                if self._need_mapping(".".join(module[0:2]), line):
                    maps = {
                        "six": ".".join(module[0:2]),
                        "py3": self.get_py3_module_mapping(line)
                    }
                    if maps not in self._mapping:
                        self._mapping.append(maps)
                if self._need_mapping("_".join(module[0:2]), line):
                    maps = {
                        "six": "_".join(module[0:2]),
                        "py3": self.get_py3_module_mapping(line)
                    }
                    if maps not in self._mapping:
                        self._mapping.append(maps)
                    if "_" in module[-1]:
                        name = module[-1].split("_")
                        tmp_module = module[0:-1]
                        tmp_module.extend(name)
                        if module == ['six', 'moves', 'urllib', 'parse']:
                            print("BOOOOOOOOMMMMMMM")
                            print(module)
                    maps = {
                        "six": ".".join(tmp_module[0:2]),
                        "py3": self.get_py3_module_mapping(line)
                    }
                    if maps not in self._mapping:
                        self._mapping.append(maps)
        print(self._mapping)

    def resolve(self, moved_module_name):
        for el in self._mapping:
            print(el)
            if el['six'] == moved_module_name:
                return el['py3']
        raise SixectomyCompatibilityNotFound(
            f"module {moved_module_name} not found")
