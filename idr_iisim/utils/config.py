__package__ = "utils"

import json
import os
from dataclasses import dataclass
import yaml
from idr_iisim.utils.logger import i_logger


@dataclass
class Config:
    foo: str = "default_foo"


class GlobalVariables:
    config_path: str
    config: Config

    def __init__(self) -> None:
        self.config_path = os.environ.get("CONFIG_PATH", "/home/ivan/Desktop/IDR/IDR-IIsim/config")

        # read config file
        try:
            config_file: str = self.config_path + "/config.yaml"
            with open(config_file) as file:
                data: dict = yaml.safe_load(file)
            self.config = Config(**data)
        except Exception as e:
            i_logger.logger.error("failed to read config file: " + str(e))
            raise e


global_variables = GlobalVariables()
