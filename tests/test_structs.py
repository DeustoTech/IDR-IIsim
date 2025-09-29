"""Test module for structs"""

import unittest

from idr_iisim.utils.structs import (
    ConstantStruct,
    DemandStruct,
    InputStruct,
    MetaDemandStruct,
    MetaStruct,
    ModelStruct,
    OutcomeStruct,
    OutputStruct,
    json_to_meta_struct,
    json_to_model_struct,
)

# model data test
MODEL_DATA = {
    "id": "Industry-process-name",
    "name": "Process name",
    "short_name": "processname",
    "type": "process",
    "description": "Description of the process",
    "version": "1.0.0",
    "debug": False,
    "constants": [
        {
            "name": "CONSTANT1",
            "description": "Description of constant 1",
            "citation": "text",
            "source": "somewhere",
            "value": 0.38,
            "units": "p.u.",
        },
        {
            "name": "CONSTAST2",
            "description": "Description of constant 2",
            "citation": "text",
            "source": "somewhere",
            "value": 0.02693,
            "units": "MJ/kg",
        },
        {
            "name": "CONSTANT3",
            "description": "Description of constant 3",
            "citation": "text",
            "source": "somewhere",
            "value": 0.1871,
            "units": "p.u.",
        },
    ],
    "inputs": [
        {
            "name": "input1",
            "description": "Description of input 1",
            "value": None,
            "units": "kt",
            "from": "Industry-process-name2",
        },
        {
            "name": "input2",
            "description": "Description of input 2",
            "value": None,
            "units": "m3",
            "from": None,
        },
        {
            "name": "input3",
            "description": "Description of input 3",
            "value": None,
            "units": "kt",
            "from": None,
        },
        {
            "name": "input4",
            "description": "Description of input 4",
            "value": None,
            "units": "GJ",
            "from": None,
        },
        {
            "name": "input5",
            "description": "Description of input 5",
            "value": None,
            "units": "kt",
            "from": "Industry-process-name2",
        },
    ],
    "outputs": [
        {
            "name": "output1",
            "operation": "input1",
            "args": [{"name": "input1", "type": "inputs"}],
            "description": "Description output 1",
            "value": None,
            "units": "kt",
        },
        {
            "name": "heat_losses_oven",
            "operation": "input3  * CONSTANT2 * CONSTANT3",
            "args": [
                {"name": "input3", "type": "inputs"},
                {"name": "CONSTANT2", "type": "constants"},
                {"name": "CONSTANT3", "type": "constants"},
            ],
            "description": "Description output 2",
            "value": None,
            "units": "GJ",
        },
        {
            "name": "input1",
            "operation": "input1 * ( 1 - CONSTANT1 )",
            "args": [
                {"name": "input1", "type": "inputs"},
                {"name": "CONSTANT1", "type": "constants"},
            ],
            "description": "Description output 3",
            "value": None,
            "units": "kt",
        },
    ],
}

# Meta data test
META_DATA = {
    "id": "Industry-process-Meta",
    "name": "industry name",
    "short_name": "IndustryName",
    "type": "industry",
    "description": "Description of the industry",
    "version": "1.0.0",
    "debug": False,
    "constants": [
        {
            "name": "CONSTANT1",
            "description": "Description of constant 1",
            "citation": "text",
            "source": "somewhere",
            "value": 1.035,
            "units": "kt/p.u.",
        },
        {
            "name": "CONSTANT2",
            "description": "Description of constant 2",
            "citation": "text",
            "source": "somewhere",
            "value": 0.375,
            "units": "t/p.u.",
        },
        {
            "name": "CONSTANT3",
            "description": "Description of constant 3",
            "citation": "text",
            "source": "somewhere",
            "value": 0.11592,
            "units": "MJ/p.u.",
        },
        {
            "name": "CONSTANT4",
            "description": "Description of constant 4",
            "citation": "text",
            "source": "somewhere",
            "value": 0.222,
            "units": "m3/p.u.",
        },
        {
            "name": "CONSTANT5",
            "description": "Description of constant 5",
            "citation": "text",
            "source": "somewhere",
            "value": 0.13,
            "units": "kt/p.u.",
        },
        {
            "name": "CONSTANT6",
            "description": "Description of constant 6",
            "citation": "text",
            "source": "somewhere",
            "value": 0.069552,
            "units": "TJ/p.u.",
        },
        {
            "name": "CONSTANT7",
            "description": "Description of constant 7",
            "citation": "text",
            "source": "somewhere",
            "value": 0.04,
            "units": "percentage/p.u.",
        },
        {
            "name": "CONSTANT8",
            "description": "Description of constant 8",
            "citation": "text",
            "source": "somewhere",
            "value": 0.135792,
            "units": "MJ",
        },
        {
            "name": "CONSTANT9",
            "description": "Description of constant 9",
            "citation": "text",
            "source": "somewhere",
            "value": 0.9,
            "units": "kt",
        },
    ],
    "inputs": [
        {
            "name": "input1",
            "description": "Description of input 1",
            "units": "kt",
            "value": None,
            "from": "Industry-process-Name1",
        },
        {
            "name": "input2",
            "description": "Description of input 2",
            "units": "kt",
            "value": None,
            "from": "Industry-process-Name2",
        },
        {
            "name": "input3",
            "description": "Description of input 3",
            "units": "kt",
            "value": None,
            "from": "Industry-process-Name1",
        },
        {
            "name": "input4",
            "description": "Description of input 4",
            "units": "kt",
            "value": None,
            "from": "Industry-process-Name3",
        },
    ],
    "outcome": [
        {
            "name": "outcome1",
            "description": "Description of outcome1",
            "units": "kt",
            "same_result": {
                "process": "Industry-process-Name3",
                "output": "cement_production",
            },
        }
    ],
    "demands": [
        {
            "name": "demand1",
            "units": "kt",
            "operation": "outcome1 * CONSTANT1",
            "used": "Industry-process-Name2",
            "args": [
                {"name": "CONSTANT1", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "description": "Description of demand 1",
        },
        {
            "name": "demand2",
            "operation": "outcome1 * CONSTANT2",
            "args": [
                {"name": "CONSTANT2", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "units": "kt",
            "used": "Industry-process-Name2",
            "description": "Description of demand 2",
        },
        {
            "name": "demand3",
            "operation": "outcome1 * CONSTANT5",
            "args": [
                {"name": "CONSTANT5", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "units": "kt",
            "description": "Description of demand 3",
            "used": "Industry-process-Name1",
        },
        {
            "name": "demand4",
            "operation": "outcome1 * CONSTANT4",
            "args": [
                {"name": "CONSTANT4", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "description": "Description of demand 4",
            "units": "m3",
            "used": "Industry-process-Name1",
        },
        {
            "name": "demand5",
            "operation": "input1 * CONSTANT7",
            "args": [
                {"name": "input1", "type": "inputs"},
                {"name": "CONSTANT7", "type": "constants"},
            ],
            "description": "Description of demand 5",
            "units": "kt",
            "used": "Industry-process-Name3",
        },
        {
            "name": "demand6",
            "operation": "outcome1 * CONSTANT3",
            "args": [
                {"name": "demand6", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "description": "Description of demand 6",
            "units": "GJ",
            "used": "Industry-process-Name2",
            "meta": "mechanical_energy",
        },
        {
            "name": "demand7",
            "operation": "outcome1 * CONSTANT6",
            "args": [
                {"name": "demand7", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "description": "Description of demand 7",
            "units": "GJ",
            "used": "Industry-process-Name1",
            "meta": "mechanical_energy",
        },
        {
            "name": "demand8",
            "operation": "outcome1 * CONSTANT8",
            "args": [
                {"name": "demand8", "type": "constants"},
                {"name": "outcome1", "type": "outcome"},
            ],
            "description": "Description of demand 8",
            "units": "GJ",
            "used": "Industry-process-Name3",
            "meta": "mechanical_energy",
        },
    ],
    "meta": [
        {
            "name": "meta_demand1",
            "operation": "demand6 + demand7 + demand8",
            "args": [
                {"name": "demand6", "type": "demand"},
                {"name": "demand7", "type": "demand"},
                {"name": "demand8", "type": "demand"},
            ],
            "description": "Description of meta-demand 1",
            "units": "GJ",
        }
    ],
    "outputs": [
        {
            "name": "output1",
            "operation": "outcome1 * CONSTANT9",
            "args": [{"name": "co2_emissions_oven", "type": "outcome"}],
            "description": "Description of output 1",
            "units": "kt",
        },
        {
            "name": "output2",
            "operation": "output1",
            "args": [
                {
                    "name": "output1",
                    "type": "outputs",
                    "from": "Industry-process-Name1",
                }
            ],
            "description": "Description of output 2",
            "units": "GJ",
        },
        {
            "name": "output3",
            "operation": "(input2 + input3 + input4)",
            "args": [
                {
                    "name": "input2",
                    "type": "inputs",
                    "from": "Industry-process-Name2",
                },
                {
                    "name": "input3",
                    "type": "inputs",
                    "from": "Industry-process-Name1",
                },
                {
                    "name": "input4",
                    "type": "inputs",
                    "from": "Industry-process-Name3",
                },
            ],
            "description": "Description of output 3",
            "value": None,
            "units": "kt",
        },
    ],
}


class TestStructs(unittest.TestCase):
    """Clas for testing Structs"""

    def test_json_to_model_struct_creation(self) -> None:
        """Check the creation of a ModelStruct and the transformation of the input values."""
        model_data_with_input = MODEL_DATA.copy()

        model = json_to_model_struct(model_data_with_input)

        self.assertIsInstance(model, ModelStruct)
        self.assertEqual(model.name, "Process name")
        self.assertEqual(model.short_name, "processname")
        for input_object in model.inputs:
            self.assertIsInstance(input_object, InputStruct)
        for output_object in model.outputs:
            self.assertIsInstance(output_object, OutputStruct)
        for constant_object in model.constants:
            self.assertIsInstance(constant_object, ConstantStruct)
        self.assertEqual(model.inputs[4].input_from, "Industry-process-name2")

    def test_json_to_meta_struct_creation(self) -> None:
        """Verifica la creación básica de MetaStruct y la transformación de claves de entrada."""
        meta_data_with_input = META_DATA.copy()

        meta = json_to_meta_struct(meta_data_with_input)

        self.assertIsInstance(meta, MetaStruct)
        self.assertEqual(meta.name, "industry name")
        self.assertEqual(meta.short_name, "IndustryName")
        for input_object in meta.inputs:
            self.assertIsInstance(input_object, InputStruct)
        for output_object in meta.outputs:
            self.assertIsInstance(output_object, OutputStruct)
        for constant_object in meta.constants:
            self.assertIsInstance(constant_object, ConstantStruct)
        for demand_object in meta.demands:
            self.assertIsInstance(demand_object, DemandStruct)
        for meta_demand_object in meta.meta:
            self.assertIsInstance(meta_demand_object, MetaDemandStruct)
        self.assertIsInstance(meta.outcome, OutcomeStruct)
        self.assertEqual(meta.inputs[2].input_from, "Industry-process-Name1")
