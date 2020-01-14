import glob
import os

import pep8

def is_valid_path(path):
    """To check if the path exists and if the is readable.

    @param path: The path of the file or directory
    @type path: str


    @raise IOError: If the path doesn't exists
    @raise OSError: If the path doesn't is not readable
    """
    # No need to check if is a file or a dir the both are valid
    if not os.path.exists(path):
        raise IOError("{path} is not a valid path".format(path=path))
    if not os.access(path, os.R_OK):
        raise OSError("{path} is not a readable path".format(path=path))


def python_files(path):
    pattern = "{path}/**/*.py".format(path=path)
    return glob.glob(pattern, recursive=True)


def is_pep8_valid(path):
    """Will check if module is pep8 compliant"""
    return pep8.Checker(path).check_all() == 0
