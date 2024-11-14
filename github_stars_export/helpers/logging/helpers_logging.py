"""

"""
import os
import logging

from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

from github_stars_export.helpers.helpers_datetime import get_time_formatted
from github_stars_export import __project__


def get_default_log_filename() -> str:
    """
    The name of the log file
    :return:
    """
    return f"{__project__}_{get_time_formatted()}.log"


def get_default_log_filepath() -> str:
    """
    :return: The default log file path combining the current working directory and the default log filename.
    """
    return os.path.join(os.getcwd(), get_default_log_filename())


def get_or_create_logging() -> logging.Logger:
    """
    Gets or creates a logging instance with specific handlers.

    :return: A configured Logger instance.
    """
    _logger = logging.getLogger(__name__)
    # _logger.addHandler(logging.StreamHandler())
    _logger.addHandler(
        RotatingFileHandler(os.path.join(os.getcwd(), get_default_log_filename())))
    _logger.addHandler(RichHandler(rich_tracebacks=True))
    return _logger
