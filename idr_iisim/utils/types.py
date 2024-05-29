__package__ = "utils"

from dataclasses import dataclass


@dataclass
class ArgumentStruct:
    name: str
    value: float


@dataclass
class ConstantStruct:
    name: str
    label: str
    description: str
    citation: str
    source: str
    value: float
    units: str


@dataclass
class InputStruct:
    name: str
    label: str
    description: str
    value: float
    input_from: list[str]
    units: str


@dataclass
class OutputStruct:
    name: str
    label: str
    description: str
    operation: str
    args: list[str]
    value: float | None = None


@dataclass
class ModelStruct:
    name: str
    id: str
    description: str
    version: str
    debug: str
    constants: list[ConstantStruct]
    inputs: list[InputStruct]
    outputs: list[OutputStruct]
