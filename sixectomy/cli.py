import argparse
import os
import sys
import textwrap

from sixectomy.common import is_valid_path


EPILOG = textwrap.dedent("""
    Exit status:
    - 0 if ok
    - 1 if something classical went wrong
    - 404 if a mapping is not found
    - 500 if engine fail during replacement

    These status code can allow you to automatize replacement in batch mode.

    Credits:
    - Hervé Beraud <hberaud@redhat.com>
""")


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
    parser = argparse.ArgumentParser(
        description="Utility to safely remove `six` usages from your projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG)
    parser.add_argument(
        "file",
        nargs="?",
        action=readable_path,
        help="file or path to analyze. \
              (The current working directory is default)",
        default=os.getcwd(),
    )
    parser.add_argument(
        '-i',
        '--in-place',
        action='store_true',
        help="edit files in place (makes backup if SUFFIX supplied)"
    )
    parser.add_argument(
        '-s',
        '--suffix',
        default=None,
        help="makes backup if SUFFIX supplied and if the `-i` flag is given"
    )
    parser.add_argument(
        "-t",
        "--report-type",
        choices=["simple", "advanced"],
        default="simple",
        help="type of report to display",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="only display the sixectomy version number",
    )
    return parser
