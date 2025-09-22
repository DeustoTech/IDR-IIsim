"""Module to process the meta.yaml, the industry's configuration"""

import os
from functools import partial
from string import Template

from sympy import parse_expr

from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.types import (
    ConstantStruct,
    DemandStruct,
    InputStruct,
    MetaDemandStruct,
    OutcomeStruct,
    OutputStruct,
    json_to_meta_struct,
)


class Meta:  # pylint: disable=too-many-instance-attributes
    """Meta class"""

    def __init__(self, yaml_data: dict, path: str):
        self.directory = os.path.dirname(path)
        self.inputs: dict[str, InputStruct] = {}
        self.outcome: dict[str, OutcomeStruct] = {}
        self.demands: dict[str, DemandStruct] = {}
        self.meta_demands: dict[str, MetaDemandStruct] = {}
        self.outputs: dict[str, OutputStruct] = {}
        self.constants: dict[str, ConstantStruct] = {}

        # Parse data
        i_logger.debug("parsing %s", yaml_data["name"])
        self.config = json_to_meta_struct(yaml_data)

        self.functions_map = {}

        items = [d for d in self.config.demands if d.meta is None]
        items += list(self.config.meta)
        items += list(self.config.outputs)

        for item in items:
            operation = parse_expr(item.operation)
            f = partial(lambda op, **kwargs: op.subs(kwargs), op=operation)
            key = item.name
            self.functions_map[key] = {
                "function": f,
                "args": item.args,
                "expression": operation,
                "description": item.description,
            }

        # Parse constants
        for constant in self.config.constants:
            self.constants[constant.name] = constant
            if constant.range and not (
                constant.range[0] <= constant.value <= constant.range[-1]
            ):
                raise ValueError(
                    f"Constant '{constant.name}' in process "
                    + f"'{self.config.name}' is not inside the valid range"
                    + f" ({constant.value} not inside {constant.range})"
                )

        # Parse outputs
        for output in self.config.outputs:
            self.outputs[output.name] = output

        # Parse demands
        for demand in self.config.demands:
            self.demands[demand.name] = demand
        # Parse meta demands
        for demand in self.config.meta:
            self.meta_demands[demand.name] = demand

        self.outcome[self.config.outcome.name] = self.config.outcome

        # Parse inputs
        for input_field in self.config.inputs:
            self.inputs[input_field.name] = input_field
            if input_field.range:
                for value in input_field.value:
                    if (
                        value < input_field.range[0]
                        or value > input_field.range[-1]
                    ):
                        raise ValueError(
                            f"Input '{input_field.name}' in process "
                            + f"'{self.config.name}' is not inside the valid range"
                            + f" ({input_field.value} not inside {input_field.range})"
                        )

    def constants_generator(self) -> str:
        """generator of the constants of the industry"""
        constants_code = ""

        # Generate constants dynamically from model configuration
        constants_code = "\n".join(
            f"{constant.name} = {constant.value}  # {constant.description}"
            for constant in self.config.constants
        )
        if constants_code:
            constants_code = (
                f"# {self.config.name}'s constants\n" + constants_code
            )

        return constants_code

    def getters_generator(self) -> str:
        """Generate getter methods"""
        getters = []

        # Load the template content
        template_path = "templates/template_generated_getter.txt"
        try:
            with open(template_path, "r", encoding="utf-8") as template_file:
                template_content = template_file.read()
        except FileNotFoundError:
            i_logger.error("Template file not found: %s", template_path)
            raise
        except Exception as e:
            i_logger.error("Error reading template file: %r", e)
            raise

        # Outcome
        for variable_name, outputs in self.outcome.items():
            getter_template = Template(template_content)
            getter_script = getter_template.substitute(
                name=variable_name, description=outputs.description
            )
            getters.append(getter_script)

        # outputs
        for variable_name, outputs in self.functions_map.items():
            getter_template = Template(template_content)
            getter_script = getter_template.substitute(
                name=variable_name, description=outputs["description"]
            )
            getters.append(getter_script)
        return "\n".join(getters)

    def constructor_pre_generator(self, process: str) -> str:
        """Generate demand initializations"""
        process_methods = []
        # Demands
        for variable_name, values in self.demands.items():
            if values.used == process:
                expression = values.operation
                for arg in values.args:
                    if arg["type"] != "constants":
                        expression = expression.replace(
                            arg["name"], f"self.__{arg['name']}"
                        )
                method_script = f"self.__{variable_name} = {expression}"
                process_methods.append(method_script)
        return "\n        ".join(process_methods)

    def constructor_post_generator(self) -> str:
        """Generate demand initializations"""
        process_methods = []
        # Meta demands
        for variable_name, values in self.meta_demands.items():
            expression = values.operation
            for arg in values.args:
                if arg["type"] != "constants":
                    expression = expression.replace(
                        arg["name"], f"self.__{arg['name']}"
                    )
            method_script = f"self.__{variable_name} = {expression}"
            process_methods.append(method_script)
        # Outputs
        for variable_name, values in self.outputs.items():
            expression = values.operation
            for arg in values.args:
                if arg["type"] != "constants":
                    expression = expression.replace(
                        arg["name"], f"self.__{arg['name']}"
                    )
            method_script = f"self.__{variable_name} = {expression}"
            process_methods.append(method_script)
        return "\n        ".join(process_methods)

    def get_units(self) -> dict[str, str]:
        """Get the units of the demands and outputs"""
        units = {}

        for value in self.outcome.values():
            units[value.name] = value.units
        for value in self.demands.values():
            if value.meta is None:
                units[value.name] = value.units
        for value in self.meta_demands.values():
            units[value.name] = value.units
        for value in self.outputs.values():
            units[value.name] = value.units

        return units
