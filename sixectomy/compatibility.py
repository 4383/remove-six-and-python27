import re
import sys

import six

from sixectomy import exceptions


def parse_line(line):
    """Extract the function signature of MovedAttribute and MovedModule
       calling in six source code.
    """
    # To more merely understand the following regex
    # please take a look to https://regex101.com/r/yPiWr3/1
    search = r'(Moved\w+)([\("_a-zA-Z,\s.+\(\)<=>1-9]*),'
    match = re.match(search, line)
    # order is important match can be equal to None so he need
    # to be tested first to exit the and condition if is None
    # if match is None the groups attribut doesn't exist and it will raise
    # an exception
    if match and match.groups():
        return match.group(1), match.group(2)
    raise exceptions.SixectomyCompatibilityException(
        f"No pattern match with line ({line})")


def eval_line(line):
    """Generate a tuple of data from a parsing of six
       MovedAttribute and MovedModule calls and by eval function signature
       previously extracted by calling the parse_line function"""
    # Hacks to handle specific six use cases when we will extract
    # the MovedAttribute and MovedModule lines and we will eval them.
    # Indeed These lines contains python code who need to be executed
    # to generate the compatibilty matrix.
    # The python interpreter code to use to run sixectomy need to be
    # the same that the interpreter which will run the refactored code.
    # For example some six source lines looks like to:
    # MovedModule("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections"),\n  # noqa
    # So we need to interpret the python code inside the parenthesis to
    # generate a tuple which can be used to retrieve the py3 module
    # which correspond to the six binding.
    # eval with this tricks is good way to properly generate our needs.
    # six.PY34 is true if python version is equal or greater than 3.4
    PY34 = six.PY34
    __name__ = "six"
    data = eval(line)
    # Only the MovedAttribute class accept more than 5 arguments
    # so if we the tuple lenght is more than 3 we get a MovedAttribute
    # where module was maybe renamed and attribute was renamed for sure.
    # Example with getcwd and getcwdb
    if len(data) > 3:
        old = "{old_mod}.{old_attr}".format(old_mod=data[1], old_attr=data[3])
        new = "{new_mod}.{new_attr}".format(new_mod=data[2], new_attr=data[3])
        if len(data) > 4:
            new = "{new_mod}.{new_attr}".format(
                new_mod=data[2], new_attr=data[4])
        data = (data[0], old, new)
    return data


class Compatibility(list):

    _ignored = ['Module_six', 'MovedAttribute', 'MovedModule']
    _sources = []
    _mapping = {}

    def __init__(self):
        self._get_base()
        self._get_moved_modules()
        self._get_specific_submodules()
        self._read_six_sources()
        self._setup_binding()

    def _read_six_sources(self):
        with open(six.__file__) as sixfile:
            lines = sixfile.readlines()
            for index, line in enumerate(lines):
                line = line.strip()
                if not line.startswith("MovedModule(") and \
                   not line.startswith("MovedAttribute("):
                    continue
                # manage carriage return on
                # MovedAttribute and MovedModule calls
                if line[-2:] == '",':
                    line = "{start} {end}".format(
                        start=line.replace("\n", ""),
                        end=lines[index + 1].replace("\t", "").strip())
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

    def _setup_binding(self):
        for line in self._sources:
            typeof, value = parse_line(line)
            value = eval_line(value)
            for el in value:
                # Protect urllib etc... to be overrided by MovedAttribut sub
                # attributes
                if typeof == 'MovedAttribute' and \
                   el in self._mapping and \
                   'urllib' in value[-1]:
                    continue
                self._mapping.update({
                    el: {
                        "type": typeof,
                        "value": value
                    }
                })

    def lookup(self, item):
        item = item.split(".")
        reverse_lookup = self._mapping.get(item[-1], None)
        if reverse_lookup:
            return reverse_lookup
        reverse_lookup = self._mapping.get(".".join(item[-2:]), None)
        if reverse_lookup:
            return reverse_lookup
        reverse_lookup = self._mapping.get("_".join(item[-2:]), None)
        if reverse_lookup:
            return reverse_lookup
        raise exceptions.SixectomyCompatibilityNotFound(
            f"unsuccessful reverse lookup ({item})")

    def get_the_python3_binding(self, item):
        return self.lookup(item)['value'][-1]
