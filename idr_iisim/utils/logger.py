__package__ = "utils"

import logging
import os


class CustomLogger:
    logger: logging.Logger

    def __init__(self, name: str) -> None:
        level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


i_logger = CustomLogger("iDesignRES")
