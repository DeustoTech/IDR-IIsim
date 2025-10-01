"""logger class"""

import logging
import os


def setup_logger(name: str) -> logging.Logger:
    """Setup the logger"""
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
