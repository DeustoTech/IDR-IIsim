"""Schema Validator"""

from typing import Any

import yaml
from jsonschema import validate


class Validator:
    """The Validator class responsible for validating data
    against schemas defined in the config schema files.

    Attributes:
        industry_validator (dict[str, Any]): Schema loaded from config/industry.yaml.
        process_validator (dict[str, Any]): Schema loaded from config/process.yaml.
    """

    # A dictionary that stores the schema loaded from the industry.yaml file
    industry_validator: dict[str, Any]
    # A dictionary that stores the schema loaded from the process.yaml file
    process_validator: dict[str, Any]

    def __init__(self) -> None:
        """Initialize the Validator by loading schemas from specified YAML files.

        Raises:
            Exception: If there is an error loading the schema files.
        """
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
        """Validate the provided data against the appropriate schema.

        This method checks if the given dictionary data conforms
        to a schema loaded from the corresponding YAML file.

        Args:
            data (dict[str, Any]): The dictionary containing data to be validated.

        Raises:
            ValueError: If the data is missing a type field or has an invalid type.
            Exception: If the validation process fails.
        """
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
