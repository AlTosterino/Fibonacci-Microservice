import logging
from os import getcwd
from pathlib import Path
import attr


FILE_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
STREAM_LOG_FORMAT = "[%(levelname)s]: %(message)s"
DEBUG_LOG_FILENAME = "debug.log"
BASE_DIR = Path(getcwd())


@attr.s(frozen=True)
class Settings:
    api: bool = attr.ib()
    consumer: bool = attr.ib()
    generator: bool = attr.ib()
    generator_delay: int = attr.ib()
    debug_filepath: str = attr.ib()
    base_dir: str = attr.ib(default=BASE_DIR)

    @classmethod
    def from_args(cls, args) -> "Settings":
        """Method to create class with provided argparse.Namespace parameters"""
        pass

    def setup_log(self) -> None:
        """Function to create basic config for logging"""
        handlers = []
        stream_log_handler = logging.StreamHandler()
        stream_log_handler.setFormatter(logging.Formatter(STREAM_LOG_FORMAT))
        stream_log_handler.setLevel(logging.INFO)
        handlers.append(stream_log_handler)
        if self.debug_filepath:
            debug_filepath = self.debug_filepath
            debug_filepath.mkdir(exist_ok=True, parents=True)
            log_filepath = debug_filepath / DEBUG_LOG_FILENAME
            file_log_handler = logging.FileHandler(log_filepath)
            file_log_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))
            file_log_handler.setLevel(logging.DEBUG)
            handlers.append(file_log_handler)
        logging.basicConfig(
            level=logging.DEBUG, handlers=handlers,
        )
