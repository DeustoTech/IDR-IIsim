"""models_dict testing module"""

import unittest
from unittest.mock import MagicMock

from idr_iisim.models.meta import Meta
from idr_iisim.models.process import Process
from idr_iisim.utils.models_dict import Industry


class TestIndustry(unittest.TestCase):
    """class for testing Industry class"""

    def setUp(self):
        """Setup that runs before each test."""
        meta_mock = MagicMock(spec=Meta)

        # Mock for the 'config' attribute of Meta
        config_mock = MagicMock()
        config_mock.name = "Meta"  # Config name
        config_mock.inputs = (
            []
        )  # Here you can mock the inputs according to the test
        meta_mock.config = config_mock  # Assign the 'config' mock to 'meta'
        # Mock of demands (if needed for the test)
        meta_mock.demands = (
            {}
        )  # Or mock it according to your test requirements

        # Pass the 'meta_mock' to the industry constructor
        self.industry = Industry(meta=meta_mock)

        # Mock of 'Process' objects
        config_mock1 = MagicMock()
        config_mock1.inputs = (
            []
        )  # Here you can mock the inputs according to the test
        process1_mock = MagicMock(spec=Process)
        process1_mock.config = config_mock1
        self.process_1 = process1_mock
        config_mock2 = MagicMock()
        config_mock2.inputs = (
            []
        )  # Here you can mock the inputs according to the test
        process2_mock = MagicMock(spec=Process)
        process2_mock.config = config_mock2
        self.process_2 = process2_mock

        # Add the processes to the industry
        self.industry.add_process("process_1", self.process_1)
        self.industry.add_process("process_2", self.process_2)

    def test_check_types_success(self):
        """Test that verifies check_types works correctly when units are consistent."""

        # Mock the objects and their properties
        mock_input = MagicMock()
        mock_input.input_from = None  # No dependency
        mock_input.units = "kg"

        self.process_1.config.inputs = [mock_input]
        self.process_1.config.name = "process_1"
        self.process_1.outputs = {"output_1": MagicMock(units="kg")}

        # Mock Meta so no errors are thrown
        self.industry.meta.config.name = "Meta"
        self.industry.meta.config.inputs = [mock_input]
        self.industry.meta.demands = {}  # No demands for now

        # If the units are consistent, no exception should be raised
        try:
            self.industry.check_types()
        except ValueError:
            self.fail("check_types raised an unexpected exception")

    def test_check_types_unit_mismatch(self):
        """Test that verifies check_types raises an exception when units do not match."""

        # Mock the objects and their properties
        mock_input = MagicMock()
        mock_input.input_from = "process_1"  # Depends on another process
        mock_input.units = "kg"

        self.process_1.config.inputs = [mock_input]
        self.process_1.config.name = "process_1"
        self.process_1.outputs = {"output_1": MagicMock(units="m")}

        self.process_2.config.inputs = [mock_input]
        self.process_2.config.name = "process_2"

        # Mock Meta so no errors are thrown
        self.industry.meta.config.name = "Meta"
        self.industry.meta.config.inputs = [mock_input]
        self.industry.meta.demands = {}

        # Verify that a ValueError exception is raised due to inconsistent units
        with self.assertRaises(ValueError):
            self.industry.check_types()

    def test_check_types_missing_input(self):
        """Test that verifies check_types raises an exception if an input
        from one process is missing in another."""

        # Create an input that depends on a non-existent process
        mock_input = MagicMock()
        mock_input.input_from = (
            "process_1"  # Depends on a non-existent process
        )
        mock_input.units = "kg"

        self.process_1.config.inputs = [mock_input]
        self.process_1.config.name = "process_1"
        self.process_1.outputs = {"output_1": MagicMock(units="kg")}

        self.process_2.config.inputs = [mock_input]
        self.process_2.config.name = "process_2"

        # Mock Meta so no errors are thrown
        self.industry.meta.config.name = "Meta"
        self.industry.meta.config.inputs = [mock_input]
        self.industry.meta.demands = {}

        # Verify that a ValueError exception is raised due to the missing input in the source model
        with self.assertRaises(ValueError):
            self.industry.check_types()

    def test_check_types_with_demand(self):
        """Test that verifies check_types handles demands correctly."""

        # Mock demand in meta
        demand = MagicMock()
        demand.name = "demand_1"
        demand.units = "kg"
        demand.used = "process_1"  # Used in process_1

        self.industry.meta.demands = {"demand_1": demand}

        mock_input = MagicMock()
        mock_input.inputs = {"demand_1": demand}
        mock_input.input_from = None
        mock_input.units = "kg"

        self.industry.models = {
            "process_1": mock_input,
        }

        self.process_1.config.inputs = [mock_input]
        self.process_1.config.name = "process_1"
        self.process_1.outputs = {"output_1": MagicMock(units="kg")}

        # Verify that no exception is raised if the units match
        try:
            self.industry.check_types()
        except ValueError:
            self.fail("check_types raised an unexpected exception")

    def test_check_types_with_invalid_demand(self):
        """Test that verifies check_types raises an exception
        if the demand has inconsistent units."""

        # Mock demand with inconsistent units
        demand = MagicMock()
        demand.name = "demand_1"
        demand.units = "kg"
        demand.used = "process_1"  # Used in process_1

        self.industry.meta.demands = {"demand_1": demand}
        self.industry.models = {"process_1": MagicMock()}

        mock_input = MagicMock()
        mock_input.input_from = None
        mock_input.units = "kg"

        self.process_1.config.inputs = [mock_input]
        self.process_1.config.name = "process_1"
        self.process_1.outputs = {
            "output_1": MagicMock(units="m")
        }  # Inconsistent units

        # Verify that an exception is raised due to inconsistent units
        with self.assertRaises(ValueError):
            self.industry.check_types()


if __name__ == "__main__":
    unittest.main()
