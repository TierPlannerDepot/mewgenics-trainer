"""Simple logger factory with optional colouring."""
from __future__ import annotations

import logging
import sys

from colorama import Fore, Style, init as colorama_init

colorama_init()
_LEVEL_COLOURS = {
    logging.DEBUG: Fore.MAGENTA,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
}


class _Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        colour = _LEVEL_COLOURS.get(record.levelno, "")
        return f"{colour}[{record.levelname[0]}]{Style.RESET_ALL} {record.getMessage()}"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(f"mewtrainer.{name}")
    if not logger.handlers:
        h = logging.StreamHandler(sys.stderr)
        h.setFormatter(_Formatter())
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger