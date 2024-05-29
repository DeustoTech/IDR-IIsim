__package__ = "utils"

import yaml
from jsonschema import validate

from idr_iisim.utils.config import GlobalVariables


class Validator:
    validator: dict

    def __init__(self) -> None:
        # load validator from file
        path_to_config = GlobalVariables().config_path + "/schema.yaml"
        try:
            with open(path_to_config) as file:
                self.validator = yaml.safe_load(file)
        except Exception as e:
            raise e
        pass

    def validate(self, data: dict) -> None:
        # validate data
        try:
            validate(data, self.validator)
        except Exception as e:
            raise e
        pass
