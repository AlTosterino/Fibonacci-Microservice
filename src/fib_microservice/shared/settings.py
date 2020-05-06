import logging
from os import getcwd
from pathlib import Path
import attr
import yaml


FILE_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
STREAM_LOG_FORMAT = "[%(levelname)s]: %(message)s"
DEBUG_LOG_FILENAME = "debug.log"
BASE_DIR = Path(getcwd())


@attr.s(frozen=True, auto_attribs=True)
class ApiSettings:
    host: str
    port: int


@attr.s(frozen=True, auto_attribs=True)
class GeneratorSettings:
    delay: int
    generator: object = attr.ib(default=None)

    def __attrs_post_init__(self):
        from fib_microservice.infrastructure.fibonacci_generator.generator import (
            FibonacciGenerator,
        )

        object.__setattr__(
            self, "generator", FibonacciGenerator(settings=self),
        )


@attr.s(frozen=True, auto_attribs=True)
class ConsumerSettings:
    host: str


@attr.s(frozen=True)
class Settings:
    api: ApiSettings = attr.ib()
    consumer: ConsumerSettings = attr.ib()
    generator: GeneratorSettings = attr.ib()
    debug_dirpath: str = attr.ib()
    base_dir: str = attr.ib(default=BASE_DIR)

    @classmethod
    def from_yaml(cls, args) -> "Settings":
        """Method to create Settings with provided YAML file"""
        with open(args.config) as file:
            conf = yaml.safe_load(file)
        if conf["debug_dirpath"]:
            conf["debug_dirpath"] = BASE_DIR / Path(conf["debug_filepath"]).expanduser()
        conf["api"] = ApiSettings(**conf["api"])
        conf["generator"] = GeneratorSettings(**conf["generator"])
        conf["consumer"] = ConsumerSettings(**conf["consumer"])
        return cls(**conf)

    def setup_log(self) -> None:
        """Function to create basic config for logging"""
        handlers = []
        stream_log_handler = logging.StreamHandler()
        stream_log_handler.setFormatter(logging.Formatter(STREAM_LOG_FORMAT))
        stream_log_handler.setLevel(logging.INFO)
        handlers.append(stream_log_handler)
        if self.debug_dirpath:
            debug_dirpath = self.debug_dirpath
            debug_dirpath.mkdir(exist_ok=True, parents=True)
            log_filepath = debug_dirpath / DEBUG_LOG_FILENAME
            file_log_handler = logging.FileHandler(log_filepath)
            file_log_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))
            file_log_handler.setLevel(logging.DEBUG)
            handlers.append(file_log_handler)
        logging.basicConfig(
            level=logging.DEBUG, handlers=handlers,
        )
