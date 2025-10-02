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


class TestIntegration(unittest.TestCase):
    """Loger test class"""

    def test_full_integration(self) -> None:
        """Full test"""
        industries_path = "Sources"
        for elem in os.listdir(industries_path):
            elem_path = os.path.join(industries_path, elem)
            if os.path.isdir(elem_path):
                process_industry(elem, elem_path)
                yaml = _find_industry(elem_path)
                output_path = os.path.join(
                    "industries", f"{yaml['short_name'].lower()}.py"
                )
                # Check if file is created
                self.assertTrue(os.path.isfile(output_path))
                # Check to import the class
                try:
                    module = importlib.import_module(
                        f"industries.{yaml['short_name'].lower()}"
                    )
                    industry_cls = getattr(module, yaml["short_name"], None)
                    self.assertIsNotNone(
                        industry_cls, "The industry has not been created"
                    )
                    tests = yaml["outcome"][0].get("tests", [1])
                    for i in range(len(tests)):
                        instance = industry_cls(tests[i])
                        self.assertIsNotNone(instance)
                        # Check demands
                        for demand in yaml["demands"]:
                            if "meta" not in demand:
                                method_name = f"get_{demand['name']}"
                                values = demand.get("tests", [])
                                with self.subTest(method=method_name):
                                    method = getattr(
                                        instance, method_name, None
                                    )
                                    self.assertIsNotNone(method)
                                    value = method()
                                    self.assertIsInstance(value, float)
                                    if i < len(values):
                                        self.assertEqual(
                                            values[i], round(value, 2)
                                        )
                        # Check meta-demands
                        for meta_demand in yaml["meta"]:
                            method_name = f"get_{meta_demand['name']}"
                            values = demand.get("tests", [])
                            with self.subTest(method=method_name):
                                method = getattr(instance, method_name, None)
                                self.assertIsNotNone(method)
                                value = method()
                                self.assertIsInstance(value, float)
                                if i < len(values):
                                    self.assertEqual(
                                        values[i], round(value, 2)
                                    )
                        # Check outputs
                        for output in yaml["outputs"]:
                            method_name = f"get_{output['name']}"
                            values = output.get("tests", [])
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
                except Exception:
                    self.fail("Industry not correctly generated")


def _find_industry(industry_path: str) -> dict[str, Any]:
    for file in Path(industry_path).rglob("*.yaml"):
        yaml_path = str(file)
        yaml_data: dict[str, Any] = load_yaml(yaml_path)
        if yaml_data["type"] == "industry":
            return yaml_data
    raise ValueError("Industry yaml not found!")
