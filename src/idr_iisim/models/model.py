"""Module to parse industry's processes"""

import os
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Callable, TypedDict, Union

from sympy import parse_expr

from idr_iisim.templates import load_template
from idr_iisim.utils.structs import (
    ConstantStruct,
    InputStruct,
    ItemStruct,
    MetaStruct,
    ModelStruct,
    OutputStruct,
)


class FunctionsMapType(TypedDict):
    """Type of FunctionsMap"""

    function: Callable[..., Any]
    args: list[dict[str, Any]]
    expression: str
    description: str


class Model(ABC):
    """Model class that represents a model in the system.
    It contains the model configuration, functions map, results, and external inputs.
    """

    def __init__(self, path: str):
        self.directory = os.path.dirname(path)
        self.inputs: dict[str, InputStruct] = {}
        self.outputs: dict[str, OutputStruct] = {}
        self.constants: dict[str, ConstantStruct] = {}
        self.functions_map: dict[str, FunctionsMapType] = {}
        self.config: Union[ModelStruct, MetaStruct]

    def process_config(
        self, items: list[ItemStruct], config: ModelStruct
    ) -> None:
        """Process configuration"""
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
        for constant in config.constants:
            self.constants[constant.name] = constant
            if constant.range and not (
                constant.range[0] <= constant.value <= constant.range[-1]
            ):
                raise ValueError(
                    f"Constant '{constant.name}' in process "
                    + f"'{config.name}' is not inside the valid range"
                    + f" ({constant.value} not inside {constant.range})"
                )

        # Parse outputs
        for output in config.outputs:
            self.outputs[output.name] = output

        # Parse inputs
        for input_field in config.inputs:
            self.inputs[input_field.name] = input_field
            if input_field.range:
                for value in input_field.value:
                    if (
                        value < input_field.range[0]
                        or value > input_field.range[-1]
                    ):
                        raise ValueError(
                            f"Input '{input_field.name}' in process "
                            + f"'{config.name}' is not inside the valid range"
                            + f" ({input_field.value} not inside {input_field.range})"
                        )

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

    @abstractmethod
    def get_getter_items(self) -> list[tuple[str, str]]:
        """Generate items' descriptions to configure as getters"""

    def getters_generator(self) -> str:
        """Generate getter methods"""
        getters = []

        # Load the template content
        template_path = "templates/template_generated_getter.txt"
        getter_template = load_template(template_path)

        # outputs
        for variable_name, description in self.get_getter_items():
            getter_script = getter_template.substitute(
                name=variable_name, description=description
            )
            getters.append(getter_script)

        return "\n".join(getters)
