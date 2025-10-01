"""Test industries and process"""

import unittest
from functools import partial
from unittest.mock import MagicMock, patch

import sympy

from idr_iisim.models.process import (  # type:ignore # pylint: disable=import-error
    Process,
)
from idr_iisim.utils.models_dict import (  # type:ignore # pylint: disable=import-error
    Industry,
)
from idr_iisim.utils.structs import (  # type:ignore # pylint: disable=import-error
    InputStruct,
    ModelStruct,
    OutputStruct,
)

SCRIPT = '''""" A description """
from math import inf

# Constants
NAME = "The Industry"
# Meta Constants
# P1 Constants

# units
UNITS = {
    "unit_key": "unit_val"
}

class industry_meta:
    """ industry_meta industry """

    def __init__(self, final_output):
        """ constructor """
        self.__validate_total_production(final_output)
        self.__final_output = final_output
        pre_constructor
P1_call()
        
post_constructor

    def __validate_total_production(self, final_output) -> None:
        if final_output < 0 or final_output > 100:
            raise ValueError(
                "The production should be a value between 0 and 100"
            )

process_method_P1
# Meta Getters
    def csv(self, separator: str = ";") -> None:
        """ print the industry as CSV format """
        attributes = vars(self)
        lines = [[], []]
        for name, value in attributes.items():
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                unit = UNITS[name]
                lines[0].append(name)
                lines[1].append(str(value))
                lines[0].append(name + "_unit")
                lines[1].append(unit)
        for line in lines:
            print(separator.join(line))

    def csv_header(self) -> list:
        attributes = vars(self)
        line = []
        for name in attributes:
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                unit = UNITS[name]
                line.append(f"{name} ({unit})")
        return line

    def csv_row(self) -> list:
        attributes = vars(self)
        line = []
        for name, value in attributes.items():
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                line.append(str(value))
        return line

    def __str__(self) -> str:
        final_str = NAME
        final_str += "\\n" + "-" * len(final_str) + "\\n"
        attributes = vars(self)
        for name, value in attributes.items():
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                unit = UNITS[name]
                print_name = name.replace("_", " ").title()
                final_str += f"{print_name}: {value:.2f} {unit}\\n"
        return final_str
'''


@patch("idr_iisim.models.process.json_to_model_struct", autospec=True)
@patch("sympy.parse_expr", autospec=True)
class TestModelProcessAndMeta(unittest.TestCase):
    """Test Process class"""

    def setUp(self) -> None:
        # Common configuration for tests
        self.minimal_yaml_data = {
            "name": "Test Process",
            "id": "t1",
            "type": "process",
            "constants": [],
            "inputs": [],
            "outputs": [],
        }
        self.path = "/fake/path/test.yaml"

    def test_process_init_and_config(
        self, _, mock_json_to_model_struct
    ) -> None:
        """Check Process initialization and the use of functools.partiall in process_config"""

        # 1. Configurar los mocks para devolver los objetos necesarios
        mock_config = ModelStruct(
            name="Test Process",
            id="t1",
            short_name="tp",
            category="process",
            description="",
            version="1.0",
            debug="False",
            constants=[],
            inputs=[],
            outputs=[
                OutputStruct(
                    name="out1",
                    description="desc1",
                    units="u1",
                    args=[],
                    operation="a + b",
                )
            ],
        )
        mock_json_to_model_struct.return_value = mock_config

        # 2. Generate object
        process = Process(self.minimal_yaml_data, self.path)

        # 3. Ase
        mock_json_to_model_struct.assert_called_once_with(
            self.minimal_yaml_data
        )

        # Check if the partial function was created
        self.assertIn("out1", process.functions_map)
        func_map = process.functions_map["out1"]
        self.assertIsInstance(func_map["function"], partial)
        # Check it has the SymPy object in its kwargs
        self.assertIsInstance(
            func_map["function"].keywords["op"], sympy.core.expr.Expr
        )
        self.assertEqual(str(func_map["function"].keywords["op"]), "a + b")

    def test_process_operations_generator(
        self, mock_parse_expr, mock_json_to_model_struct
    ) -> None:
        """Check that the generation of the operations script"""

        mock_config = ModelStruct(
            name="Test Process",
            id="t1",
            short_name="tp",
            category="process",
            description="",
            version="1.0",
            debug="False",
            constants=[],
            inputs=[],
            outputs=[
                OutputStruct(
                    name="total_energy",
                    description="Total energy",
                    units="J",
                    args=[
                        {"name": "cost", "type": "inputs"},
                        {"name": "C1", "type": "constants"},
                    ],
                    operation="cost * C1",
                )
            ],
        )
        mock_json_to_model_struct.return_value = mock_config

        # Simular el objeto SymPy Expression con su representación de cadena
        mock_expr = MagicMock()
        mock_expr.__str__.return_value = "cost * C1"
        mock_parse_expr.return_value = mock_expr

        process = Process(self.minimal_yaml_data, self.path)

        # La entrada (input) debe ser prefijada con 'self.__' en el código generado
        expected_script = "self.__total_energy = C1*cost"

        script = process.operations_generator()
        self.assertIn(expected_script, script)


@patch("idr_iisim.models.meta.Meta", autospec=True)
@patch("idr_iisim.models.process.Process", autospec=True)
class TestIndustry(unittest.TestCase):
    """Test industry"""

    def test_add_process_dependencies(self, _, __) -> None:
        """Check that add process builds correctly the dependencies"""

        # Mock that configuration of a process that depends on another model (M1)
        mock_config_p1 = MagicMock(spec=ModelStruct)
        mock_config_p1.id = "P1"
        mock_config_p1.inputs = [
            InputStruct(
                name="i1", description="", units="", value=[], input_from="M1"
            )
        ]

        # Mock that configuration of a process that has no dependencies
        mock_config_p2 = MagicMock(spec=ModelStruct)
        mock_config_p2.id = "P2"
        mock_config_p2.inputs = [
            InputStruct(
                name="i2", description="", units="", value=[], input_from=""
            )
        ]

        # Generate some instances with both configurations
        mock_process_1 = MagicMock(config=mock_config_p1)
        mock_process_2 = MagicMock(config=mock_config_p2)

        industry = Industry()
        industry.add_process("P1", mock_process_1)
        industry.add_process("P2", mock_process_2)

        self.assertIn("P1", industry.dependencies)
        self.assertEqual(industry.dependencies["P1"], {"M1"})
        self.assertNotIn("P3", industry.dependencies)

    def test_script_generator_calls_model_methods(
        self, mock_process, mock_meta
    ) -> None:
        """Check that the script_generator calls all the script generation methods"""

        # Mocks Meta Class
        mock_meta_config = MagicMock()
        mock_meta_config.short_name = "industry_meta"
        mock_meta_config.name = "The Industry"
        mock_meta_config.description = "A description"
        mock_meta_config.outcome.name = "final_output"
        mock_meta_config.outcome.range = [0, 100]

        mock_meta = mock_meta.return_value
        mock_meta.config = mock_meta_config
        mock_meta.get_units.return_value = {"unit_key": "unit_val"}
        # Simulate the genaration scripts
        mock_meta.constants_generator.return_value = "# Meta Constants"
        mock_meta.constructor_pre_generator.return_value = "pre_constructor\n"
        mock_meta.constructor_post_generator.return_value = (
            "\npost_constructor"
        )
        mock_meta.getters_generator.return_value = "# Meta Getters"

        # Mocks Process Class
        mock_process_config = MagicMock()
        mock_process_config.id = "P1"
        mock_process = mock_process.return_value
        mock_process.config = mock_process_config
        mock_process.process_methods_generator.return_value = (
            "process_method_P1"
        )
        mock_process.constants_generator.return_value = "# P1 Constants"
        mock_process.process_call_method_generator.return_value = "P1_call()"

        industry = Industry(meta=mock_meta)
        industry.add_process("P1", mock_process)

        # Force the execution queue to returns "P1"
        with patch(
            "idr_iisim.utils.models_dict.Industry.generate_execution_queue",
            return_value=["P1"],
        ):
            script = industry.script_generator()

        # Verifications
        mock_meta.constants_generator.assert_called_once()
        mock_process.process_methods_generator.assert_called_once()
        mock_process.constants_generator.assert_called_once()
        mock_meta.constructor_pre_generator.assert_called_once_with(
            mock_process.config.id
        )
        mock_process.process_call_method_generator.assert_called_once()
        mock_meta.constructor_post_generator.assert_called_once()

        # Check the generated script
        self.assertIsInstance(script, str)
        self.assertEqual(script, SCRIPT)
