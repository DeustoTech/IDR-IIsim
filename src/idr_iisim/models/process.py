"""Module to parse industry's processes"""

from typing import Any

from idr_iisim.models.model import Model
from idr_iisim.templates import load_template
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.structs import (
    ItemStruct,
    ModelStruct,
    json_to_model_struct,
)


class Process(Model):
    """Process class that represents a model in the system.

    It contains the model configuration, functions map, results, and external inputs.

    Attributes:
        config (ModelStruct): Holds the parsed model configuration.
    """

    def __init__(self, yaml_data: dict[str, Any], path: str):
        """Initialize the Process class with YAML data and the path.

        Args:
            yaml_data (dict[str, Any]): Parsed YAML configuration data.
            path (str): Path to the configuration file.

        Raises:
            ValueError: If there are issues in parsing the configuration.
        """
        super().__init__(path)

        # Parse data
        i_logger.debug("parsing %s", yaml_data["name"])
        self.config: ModelStruct = json_to_model_struct(yaml_data)

        items: list[ItemStruct] = list(self.config.outputs)
        self.process_config(items, self.config)

    def get_getter_items(self) -> list[tuple[str, str]]:
        """Generate items' descriptions to configure as getters.

        Returns:
            list[tuple[str, str]]: A list of tuples containing variable names
            and their descriptions.
        """
        getter_items = []

        # outputs
        for variable_name, output in self.functions_map.items():
            getter_items.append((variable_name, output["description"]))

        return getter_items

    def operations_generator(self) -> str:
        """Generate operations methods for the model.

        Returns:
            str: The generated operations as a string.
        """
        process_methods = []
        for variable_name, outputs in self.functions_map.items():
            expression = str(outputs["expression"])
            for arg in outputs["args"]:
                if arg["type"] == "outputs":
                    expression = expression.replace(
                        arg["name"], f"self.__{arg['name']}"
                    )
            method_script = f"self.__{variable_name} = {expression}"
            process_methods.append(method_script)
        return "\n        ".join(process_methods)

    def process_methods_generator(self) -> str:
        """Generate the methods for the industry's class.

        Returns:
            str: The generated methods as a formatted string.
        """
        # Load the template content
        template_path = "templates/template_generated_process_method.txt"
        method_template = load_template(template_path)

        args = []
        for outputs in self.functions_map.values():
            for arg in outputs["args"]:
                if arg["type"] == "inputs":
                    if arg["name"] not in args:
                        args.append(arg["name"])

        args_script = "self"
        if args:
            args_script += ", "
            args_script += ", ".join(args)

        return method_template.substitute(
            name=self.config.short_name,
            args=args_script,
            description=self.config.description,
            operation=self.operations_generator(),
        )

    def process_call_method_generator(self) -> str:
        """Generate the code to call the different methods.

        Returns:
            str: The generated method call as a string.
        """
        script = f"self.__{self.config.short_name}("

        args = []
        for outputs in self.functions_map.values():
            for arg in outputs["args"]:
                if arg["type"] == "inputs":
                    name = f"self.__{arg['name']}"
                    if name not in args:
                        args.append(name)

        script += ", ".join(args)
        script += ")"
        return "\n        " + script
