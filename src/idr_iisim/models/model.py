"""Module to parse industry's processes"""

import os
from functools import partial
from string import Template  # Use Template for substitution

from sympy import ImmutableDenseMatrix, Matrix, parse_expr

from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.types import (
    ConstantStruct,
    InputStruct,
    ModelStruct,
    OutputStruct,
    json_to_model_struct,
)


class Model:
    """Model class that represents a model in the system.
    It contains the model configuration, functions map, results, and external inputs.
    """

    directory: str
    config: ModelStruct
    functions_map: dict
    results: dict[str, Matrix | ImmutableDenseMatrix] = {}
    external_inputs: dict[
        str, dict[str, Matrix]
    ] = {}  # dict[model_id, dict[arg_name, value]]
    inputs: dict[str, InputStruct] = {}
    constants: dict[str, ConstantStruct] = {}
    outputs: dict[str, OutputStruct] = {}

    def __init__(self, data: dict, path: str):
        self.directory = os.path.dirname(path)
        # Parse data
        i_logger.debug("parsing %s", data["name"])
        self.config = json_to_model_struct(data)
        self.setup()

    def setup(self) -> None:
        """Reads the model configuration file and sets up the model for calculation.
        Returns: None
        """

        # read functions
        self.functions_map = {}
        for output in self.config.outputs:
            operation = parse_expr(output.operation)
            f = partial(lambda op, **kwargs: op.subs(kwargs), op=operation)
            key = output.name
            self.functions_map[key] = {
                "function": f,
                "args": output.args,
                "expression": operation,
                "description": output.description,
            }

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

        i_logger.debug("setup completed for %s", self.config.name)
        i_logger.debug("functions_map: \n%r", self.functions_map)

    def constants_generator(self) -> str:
        """generator of the constants of the process"""
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

        for variable_name, outputs in self.functions_map.items():
            getter_template = Template(template_content)
            getter_script = getter_template.substitute(
                name=variable_name, description=outputs["description"]
            )
            getters.append(getter_script)
        return "\n".join(getters)

    def operations_generator(self) -> str:
        """Generate operations"""
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
        """Generate the industry's class' methods"""
        # Load the template content
        template_path = "templates/template_generated_process_method.txt"
        try:
            with open(template_path, "r", encoding="utf-8") as template_file:
                template_content = template_file.read()
        except FileNotFoundError:
            i_logger.error("Template file not found: %s", template_path)
            raise
        except Exception as e:
            i_logger.error("Error reading template file: %r", e)
            raise

        method_template = Template(template_content)

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
        """Generator for the code to call the different methods"""
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


# run = Model()
