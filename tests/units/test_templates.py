"""templates testing module"""

import unittest
from string import Template
from unittest.mock import mock_open, patch

from idr_iisim.templates import load_template


class TestLoadTemplate(unittest.TestCase):
    """Test templates module"""

    @patch("builtins.open", new_callable=mock_open, read_data="Test ${name}")
    def test_load_template_success(self, mock_file) -> None:
        """Test that it loads correctly a template from an existing file."""
        template_path = "test_template.txt"
        template = load_template(template_path)

        self.assertIsInstance(template, Template)
        self.assertEqual(template.substitute(name="Cement"), "Test Cement")
        mock_file.assert_called_once_with(template_path, "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_template_file_not_found(self, _) -> None:
        """Test that it raises a FileNotFoundError if the file does not exist."""
        template_path = "non_existent_template.txt"
        with self.assertRaises(FileNotFoundError):
            load_template(template_path)

    @patch("builtins.open", new_callable=mock_open)
    def test_load_template_read_error(self, mock_file) -> None:
        """Test that it raises an Exception if there is any error reading the file."""
        mock_file.side_effect = IOError("Read Error")
        template_path = "test_template.txt"

        with self.assertRaises(Exception):
            load_template(template_path)


if __name__ == "__main__":
    unittest.main()
