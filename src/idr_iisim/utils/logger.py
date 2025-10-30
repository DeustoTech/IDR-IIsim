"""logger class"""

import logging
import os


def setup_logger(name: str) -> logging.Logger:
    """Setup the logger with a specified name.

    This function configures a logger that outputs log messages to the
    console with a specified log level.
    The log level can be set via the environment variable "LOG_LEVEL",
    defaulting to DEBUG if not set.

    Args:
        name (str): Name of the logger to be created.

    Returns:
        logging.Logger: Configured Logger instance.
    """
    level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


i_logger = setup_logger("iDesignRES")
