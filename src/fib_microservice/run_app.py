import argparse
import sys
import logging

from fib_microservice import __version__
from fib_microservice.shared.settings import Settings

__author__ = "AlTosterino"
__copyright__ = "AlTosterino"
__license__ = "mit"

log = logging.getLogger(__name__)


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


def main(settings: Settings) -> None:
    """Main entry point allowing external calls

    Args:
        settings ([Settings]): Settings object
    """
    log.debug("Launched")


def parse_args():
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="fib_microservice {ver}".format(ver=__version__),
    )
    parser.add_argument("--debug", help="Debug file", type=str, metavar="Path")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--generator", nargs="?", const=3, type=int)
    group.add_argument("-c", "--consumer", action="store_true")
    group.add_argument("-a", "--api", action="store_true")
    return parser.parse_args()


def run():
    """Entry point for console_scripts"""
    args = parse_args()
    settings = Settings.from_args()
    settings.setup_log()
    main(settings)


if __name__ == "__main__":
    run()
