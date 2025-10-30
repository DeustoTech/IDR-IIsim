"""module to load templates"""

from string import Template  # Use Template for substitution

from idr_iisim.utils.logger import i_logger


def load_template(template_path: str) -> Template:
    """Load a template from the specified file path.

    This function reads the content of the given template file and returns a Template object
    that can be used for string substitution.

    Args:
        template_path (str): Path to the template file to be loaded.

    Returns:
        Template: A Template object containing the loaded template content.

    Raises:
        FileNotFoundError: If the specified template file does not exist.
        Exception: If there is an error reading the template file (e.g., encoding issues).
    """
    try:
        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        i_logger.error("Template file not found: %s", template_path)
        raise
    except Exception as e:
        i_logger.error("Error reading template file: %r", e)
        raise
    return Template(template_content)
