import logging

from f1.config import Config
from f1.enums import Formula1Enum


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(Formula1Enum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(config: Config):
    log_level = str(config.LOG_LEVEL).upper()  # cast to string
    log_levels = list(LogLevels)

    if log_level not in log_levels:
        # we use error as the default log level
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
