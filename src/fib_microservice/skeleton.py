import argparse
import sys
import logging

from fib_microservice import __version__

__author__ = "AlTosterino"
__copyright__ = "AlTosterino"
__license__ = "mit"


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


def parse_args(args):
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--generator", action="store_true")
    group.add_argument("-c", "--consumer", action="store_true")
    group.add_argument("-a", "--api", action="store_true")
    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    print(args)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
