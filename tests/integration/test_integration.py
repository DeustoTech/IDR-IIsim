"""Full integration test"""

import importlib
import os
import unittest
from pathlib import Path
from typing import Any

from idr_iisim.utils.models_dict import (  # type:ignore # pylint: disable=import-error
    load_yaml,
)
from main import process_industry  # type:ignore # pylint: disable=import-error

INDUSTRIES_PATH = "Sources"


class TestIntegration(unittest.TestCase):
    """Loger test class"""

    def test_full_integration(self) -> None:
        """Full test"""
        for elem in os.listdir(INDUSTRIES_PATH):
            elem_path = os.path.join(INDUSTRIES_PATH, elem)
            if os.path.isdir(elem_path):
                process_industry(elem, elem_path)
                yaml = _find_industry(elem_path)
                # Check if file is created
                self.assertTrue(
                    os.path.isfile(
                        _get_industry_class_path(yaml["short_name"])
                    )
                )
                # Check to import the class
                try:
                    industry_cls = _import_class(yaml["short_name"])
                    self.assertIsNotNone(
                        industry_cls, "The industry has not been created"
                    )
                    tests = yaml["outcome"][0].get("tests", [1])
                    for i in range(  # pylint: disable=consider-using-enumerate
                        len(tests)
                    ):
                        instance = industry_cls(tests[i])
                        self.assertIsNotNone(instance)
                        # Check items (demands, meta-demands and outputs)
                        items_to_evaluate = [
                            demand
                            for demand in yaml["demands"]
                            if "meta" not in demand
                        ]
                        items_to_evaluate.extend(yaml["meta"])
                        items_to_evaluate.extend(yaml["outputs"])
                        for item in items_to_evaluate:
                            method_name = f"get_{item['name']}"
                            values = item.get("tests", [])
                            with self.subTest(method=method_name):
                                method = getattr(instance, method_name, None)
                                self.assertIsNotNone(method)
                                value = method()
                                self.assertIsInstance(value, float)
                                if i < len(values):
                                    self.assertEqual(
                                        values[i], round(value, 2)
                                    )
                        # Check other methods
                        string_repr = str(instance)
                        self.assertIsInstance(string_repr, str)
                        self.assertEqual(
                            string_repr.split("\n", maxsplit=1)[0],
                            f"{yaml['short_name']} industry",
                        )
                        self.assertIsNone(instance.csv())
                        self.assertIsInstance(instance.csv_header(), list)
                        self.assertIsInstance(instance.csv_row(), list)
                except Exception:  # pylint: disable=broad-exception-caught
                    self.fail("Industry not correctly generated")


def _find_industry(industry_path: str) -> dict[str, Any]:
    for file in Path(industry_path).rglob("*.yaml"):
        yaml_path = str(file)
        yaml_data: dict[str, Any] = load_yaml(yaml_path)
        if yaml_data["type"] == "industry":
            return yaml_data
    raise ValueError("Industry yaml not found!")


def _import_class(name: str) -> Any:
    module = importlib.import_module(f"industries.{name.lower()}")
    industry_cls = getattr(module, name, None)
    return industry_cls


def _get_industry_class_path(name: str) -> str:
    output_path = os.path.join("industries", f"{name.lower()}.py")
    return output_path
