import argparse
import multiprocessing
from argparse import HelpFormatter
from operator import attrgetter
from app.core import definitions
from app.core import values


class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


def parse_args():
    parser = argparse.ArgumentParser(
        prog=values.tool_name,
        usage="%(prog)s [options]",
        formatter_class=SortingHelpFormatter,
    )
    parser._action_groups.pop()
    required = parser.add_argument_group("Required arguments")
    required.add_argument("--file", "-F", help="path to package", type=open)
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        definitions.ARG_DEBUG_MODE,
        "-d",
        help="print debugging information",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    return args
