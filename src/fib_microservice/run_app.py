import argparse
import sys
import logging

from fib_microservice import __version__
from fib_microservice.shared.settings import Settings
from fib_microservice.application.use_cases import generator, consumer, api

__author__ = "AlTosterino"
__copyright__ = "AlTosterino"
__license__ = "mit"

log = logging.getLogger(__name__)


def parse_args():
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Fibonacci microservice")
    parser.add_argument(
        "--version",
        action="version",
        version="fib_microservice {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-c",
        "--config",
        help="YAML config file",
        type=str,
        metavar="Path",
        required=True,
    )
    return parser.parse_args()


def configure_settings(args: argparse.Namespace) -> Settings:
    settings = Settings.from_yaml(args)
    settings.setup_log()
    return settings


def run_generator() -> None:
    """Entry point for generator"""
    args = parse_args()
    settings = configure_settings(args)
    log.info("Launching generator")
    try:
        generator.main(settings.generator)
    except Exception as e:
        log.exception(e)


def run_consumer() -> None:
    """Entry point for consumer"""
    args = parse_args()
    settings = configure_settings(args)
    log.info("Launching consumer")
    try:
        consumer.main(settings.consumer)
    except Exception as e:
        log.exception(e)


def run_api() -> None:
    """Entry point for api"""
    args = parse_args()
    settings = configure_settings(args)
    log.info("Launching api")
    try:
        api.main(settings.api)
    except Exception as e:
        log.exception(e)
