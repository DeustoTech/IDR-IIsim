"""Schema Validator"""

from typing import Any

import yaml
from jsonschema import validate


class Validator:
    """The Validator class that is responsible for validating data
    against a schema defined in a config/schema.yaml file"""

    # A dictionary that stores the schema loaded from the industry.yaml file
    industry_validator: dict[str, Any]
    # A dictionary that stores the schema loaded from the process.yaml file
    process_validator: dict[str, Any]

    def __init__(self) -> None:
        """load validator from file: Ensures that data adheres
        to the structure and constraints defined in the schema.yaml"""
        path_to_config = "config/industry.yaml"
        try:
            with open(path_to_config, encoding="utf-8") as file:
                # load schema from file (schema.yaml)
                # and store it in the validator attribute
                self.industry_validator = yaml.safe_load(file)
        except Exception as e:
            raise e
        path_to_config = "config/process.yaml"
        try:
            with open(path_to_config, encoding="utf-8") as file:
                # load schema from file (process.yaml)
                # and store it in the validator attribute
                self.process_validator = yaml.safe_load(file)
        except Exception as e:
            raise e

    def validate(self, data: dict[str, Any]) -> None:
        """validate data, check if a given dictionary (data) conforms
        to a schema loaded from a schema.yaml file"""
        try:
            if "type" not in data:
                raise ValueError("YAML should have a type field")
            if data["type"] not in ["industry", "process"]:
                raise ValueError(
                    "YAML's type field should be 'industry' or 'process'"
                )
            schema = self.process_validator
            if data["type"] == "industry":
                schema = self.industry_validator
            validate(instance=data, schema=schema)
        except Exception as e:
            raise e

    def print_industry_schema(self) -> None:
        """print current validation schema"""
        print(self.industry_validator)

    def print_process_schema(self) -> None:
        """print current validation schema"""
        print(self.process_validator)
