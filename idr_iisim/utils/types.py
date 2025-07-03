__package__ = "utils"

import math
from dataclasses import dataclass, field
from typing import Optional


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
    range: Optional[list[float]] = None


@dataclass
class InputStruct:
    name: str
    label: str
    description: str
    value: list[float]
    input_from: str = field(metadata={"json_key": "from"})
    units: str
    range: Optional[list[float]] = None


@dataclass
class OutputStruct:
    name: str
    label: str
    description: str
    operation: str
    args: list[str]
    units: str
    value: Optional[float] = None
    range: Optional[list[float]] = None


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


def json_to_model_struct(data: dict) -> ModelStruct:
    constants = [ConstantStruct(**const) for const in data["constants"]]
    inputs = [
        InputStruct(
            **{k if k != "from" else "input_from": v for k, v in inp.items()}
        )
        for inp in data["inputs"]
    ]
    outputs = [OutputStruct(**out) for out in data["outputs"]]

    model = ModelStruct(
        name=data["name"],
        id=data["id"],
        description=data["description"],
        version=data["version"],
        debug=data["debug"],
        constants=constants,
        inputs=inputs,
        outputs=outputs,
    )

    return model
