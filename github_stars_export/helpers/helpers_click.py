"""

"""
import rich_click as click
from rich.console import Console

_package_console: click.Console = None


def get_or_create_package_console() -> click.Console:
    """
    Get or create the package console if it does not exist.
    :return:
    """
    global _package_console
    if not _package_console:
        _package_console = Console(highlight=False)

    return _package_console


def _console_out():
    return


def console_info(message, *messages):
    """
    Write out the info message.
    :param message:
    :param messages:
    :return:
    """
    if not message:
        pass


def console_warning(message, *messages):
    """
    Write out the info message.
    :param message:
    :param messages:
    :return:
    """
    if not message:
        pass


def console_error(message, *messages):
    """
    Write out the info message.
    :param message:
    :param messages:
    :return:
    """
    if not message:
        pass


def console_exception(message, *, exc: Exception):
    """
    Write out the info message.
    :param exc:
    :param message:
    :param messages:
    :return:
    """
    if not message:
        pass
