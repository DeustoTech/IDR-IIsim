"""Testing utils"""

import logging
import unittest
from string import Template
from unittest.mock import MagicMock, mock_open, patch

from idr_iisim.templates import (  # type:ignore # pylint: disable=import-error
    load_template,
)
from idr_iisim.utils.logger import (  # type:ignore # pylint: disable=import-error
    setup_logger,
)


class TestLogger(unittest.TestCase):
    """Loger test class"""

    @patch("os.environ.get", return_value="INFO")
    def test_setup_logger_level(self, _: MagicMock) -> None:
        """Check that the logger is configured with
        the correct level of the environment variable"""
        logger_name = "test_info"
        logger = setup_logger(logger_name)

        self.assertEqual(logger.name, logger_name)
        self.assertEqual(logger.level, logging.INFO)
        # También se puede verificar que el handler tenga el nivel INFO
        self.assertEqual(logger.handlers[0].level, logging.INFO)


class TestTemplates(unittest.TestCase):
    """Template test class"""

    def test_load_template_success(self) -> None:
        """Check that function loads the file and returns a Template object"""
        mock_file_content = "The result is $value."
        m = mock_open(read_data=mock_file_content)

        with patch("builtins.open", m):
            template = load_template("templates/test.txt")

            self.assertIsInstance(template, Template)
            self.assertEqual(
                template.substitute(value="42"), "The result is 42."
            )
            m.assert_called_once_with(
                "templates/test.txt",
                "r",
                encoding="utf-8",
            )

    @patch("idr_iisim.templates.i_logger", autospec=True)
    def test_load_template_file_not_found(
        self, mock_logger: MagicMock
    ) -> None:
        """Check that a FileNotFoundError is raised if
        the file does not exist
        """
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = FileNotFoundError
            with self.assertRaises(FileNotFoundError):
                load_template("templates/non_existent_path.txt")

            mock_logger.error.assert_called_once_with(
                "Template file not found: %s",
                "templates/non_existent_path.txt",
            )

    @patch("idr_iisim.templates.i_logger", autospec=True)
    def test_load_template_generic_exception(
        self, mock_logger: MagicMock
    ) -> None:
        """Check that a generic exception is raised and
        the error registered by the logger"""
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = IOError("Simulated IO Error")
            with self.assertRaises(IOError):
                load_template("some_path.txt")

            mock_logger.error.assert_called_once()
            self.assertTrue(
                str(mock_logger.error.call_args[0][0]).startswith(
                    "Error reading template file:"
                )
            )
