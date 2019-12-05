from sys import exit
from sys import version_info

from pbr.version import VersionInfo

from sixectomy import cli
from sixectomy import surgery
from sixectomy.exceptions import SixectomyException
from sixectomy.models import Analyze
from sixectomy.reports import Report


def main():
    if version_info[0] < 3:
        print("Sixectomy must be run in a python 3 environment")
        sys.exit(125)
    args = cli.argparser().parse_args()
    version = VersionInfo("sixectomy")
    if args.version:
        print("sixectomy v{version}".format(version=version))
        return 0
    filename = args.file
    if not filename:
        return 0

    try:
        analyze = Analyze(filename)
    except SixectomyException as err:
        print(str(err))
        return 1
    else:
        report = Report(analyze, report_type=args.report_type)
        report.rendering()
        surgerer = surgery.Operating(analyze)
        surgerer.act()
    return 0


if __name__ == "__main__":
    exit(main())
