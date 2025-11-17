"""scehma testing module"""

import unittest
from unittest.mock import mock_open, patch

from jsonschema.exceptions import ValidationError

from idr_iisim.utils.schema import Validator


class TestValidator(unittest.TestCase):
    """Unit tests for the Validator class"""

    def setUp(self) -> None:
        """Set up test cases and mock the YAML files."""
        self.validator = Validator()

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_initialize_industry_schema(self, _) -> None:
        """Test if the industry schema is loaded properly."""
        self.validator.__init__()
        self.assertIsInstance(self.validator.industry_validator, dict)

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_initialize_process_schema(self, _) -> None:
        """Test if the process schema is loaded properly."""
        self.validator.__init__()
        self.assertIsInstance(self.validator.process_validator, dict)

    def test_validate_missing_type_field(self) -> None:
        """Test validation raises ValueError for missing 'type' field."""
        with self.assertRaises(ValueError) as context:
            self.validator.validate({})
        self.assertEqual(
            str(context.exception), "YAML should have a type field"
        )

    def test_validate_invalid_type_field(self) -> None:
        """Test validation raises ValueError for invalid 'type' field."""
        with self.assertRaises(ValueError) as context:
            self.validator.validate({"type": "invalid"})
        self.assertEqual(
            str(context.exception),
            "YAML's type field should be 'industry' or 'process'",
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"type": "string"}',
    )
    @patch("idr_iisim.utils.schema.validate")
    def test_validate_industry_schema(self, mock_validate, _) -> None:
        """Test validate method for valid industry type."""
        self.validator.__init__()
        self.validator.validate(
            {"type": "industry", "name": "Test"}
        )  # Expecting no exceptions
        mock_validate.assert_called_once()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"type": "process"}',
    )
    @patch("idr_iisim.utils.schema.validate")
    def test_validate_process_schema(self, mock_validate, _) -> None:
        """Test validate method for valid process type."""
        self.validator.__init__()
        self.validator.validate(
            {"type": "process", "name": "Test"}
        )  # Expecting no exceptions
        mock_validate.assert_called_once()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"type": "industry"}',
    )
    @patch("idr_iisim.utils.schema.validate")
    def test_validate_invalid_data(self, mock_validate, _) -> None:
        """Test validate method raises exception for invalid data."""
        mock_validate.side_effect = ValidationError("Invalid data")
        with self.assertRaises(ValidationError):
            self.validator.validate({"type": "industry"})

    def test_print_industry_schema(self) -> None:
        """Test print_industry_schema method."""
        with patch("builtins.print") as mocked_print:
            self.validator.print_industry_schema()
            mocked_print.assert_called_once_with(
                self.validator.industry_validator
            )

    def test_print_process_schema(self) -> None:
        """Test print_process_schema method."""
        with patch("builtins.print") as mocked_print:
            self.validator.print_process_schema()
            mocked_print.assert_called_once_with(
                self.validator.process_validator
            )


if __name__ == "__main__":
    unittest.main()
