"""

"""
import os
import logging

from logging.handlers import RotatingFileHandler

from github_stars_export.helpers.helpers_datetime import get_time_formatted
from github_stars_export import __project__


def get_or_create_logging() -> logging.Logger:
    """
    Get or instantiate the logging instance.
    :return:
    """
    _logger = logging.getLogger(__name__)
    _logger.addHandler(logging.StreamHandler())
    _logger.addHandler(
        RotatingFileHandler(os.path.join(os.getcwd(), f"{__project__}_{get_time_formatted()}.log")))
    return _logger
