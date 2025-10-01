"""Schema Validator"""

from typing import Any

import yaml
from jsonschema import validate


class Validator:
    """The Validator class that is responsible for validating data
    against a schema defined in a config/schema.yaml file"""

    validator: dict[
        str, Any
    ]  # A dictionary that stores the schema loaded from the schema.yaml file

    def __init__(self) -> None:
        """load validator from file: Ensures that data adheres
        to the structure and constraints defined in the schema.yaml"""
        path_to_config = "config/schema.yaml"
        try:
            with open(path_to_config, encoding="utf-8") as file:
                # load schema from file (schema.yaml)
                # and store it in the validator attribute
                self.validator = yaml.safe_load(file)
        except Exception as e:
            raise e

    def validate(self, data: dict[str, Any]) -> None:
        """validate data, check if a given dictionary (data) conforms
        to a schema loaded from a schema.yaml file"""
        try:
            validate(instance=data, schema=self.validator)
        except Exception as e:
            raise e

    def print_schema(self) -> None:
        """print current validation schema"""
        print(self.validator)
