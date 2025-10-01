"""module to load templates"""

from string import Template  # Use Template for substitution

from idr_iisim.utils.logger import i_logger


def load_template(template_path: str) -> Template:
    """load a template given the template's path"""
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
