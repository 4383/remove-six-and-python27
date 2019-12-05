import argparse
import os
import sys

from sixectomy.common import is_valid_path


class readable_path(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            is_valid_path(values)
        except (IOError, OSError) as err:
            print(str(err))
            parser.print_help()
            sys.exit(1)
        else:
            setattr(namespace, self.dest, values)


def argparser():
    parser = argparse.ArgumentParser(description="Analyze python file")
    parser.add_argument(
        "file",
        nargs="?",
        action=readable_path,
        help="Path to analyze. \
              If not provided sixectomy analyze the current working dir",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-t",
        "--report-type",
        choices=["simple", "advanced"],
        default="simple",
        help="Type of report to display",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Only display the sixectomy version number",
    )
    return parser
