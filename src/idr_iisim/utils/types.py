__package__ = "utils"

import math
from dataclasses import dataclass, field
from typing import Optional, Any


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
class OutcomeStruct:
    name: str
    label: str
    description: str
    units: str
    same_result: str


@dataclass
class DemandStruct:
    name: str
    description: str
    units: str
    operation: str
    args: list[dict[str, Any]]
    used: str
    meta: Optional[str] = None


@dataclass
class MetaDemandStruct:
    name: str
    description: str
    units: str
    operation: str
    args: list[dict[str, Any]]


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
    args: list[dict[str, Any]]
    units: str
    value: Optional[float] = None
    range: Optional[list[float]] = None


@dataclass
class ModelStruct:
    name: str
    short_name: str
    id: str
    category: str
    description: str
    version: str
    debug: str
    constants: list[ConstantStruct]
    inputs: list[InputStruct]
    outputs: list[OutputStruct]


@dataclass
class MetaStruct:
    name: str
    short_name: str
    id: str
    category: str
    description: str
    version: str
    debug: str
    inputs: list[InputStruct]
    outcome: OutcomeStruct
    constants: list[ConstantStruct]
    outputs: list[OutputStruct]
    demands: list[DemandStruct]
    meta: list[MetaDemandStruct]


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
        short_name=data["short_name"],
        category=data["type"],
        description=data["description"],
        version=data["version"],
        debug=data["debug"],
        constants=constants,
        inputs=inputs,
        outputs=outputs,
    )

    return model


def json_to_meta_struct(data: dict) -> MetaStruct:
    constants = [ConstantStruct(**const) for const in data["constants"]]
    outcome = [OutcomeStruct(**out) for out in data["outcome"]][0]
    outputs = [OutputStruct(**out) for out in data["outputs"]]
    demands = [DemandStruct(**out) for out in data["demands"]]
    meta_demands = []
    if "meta" in data:
        meta_demands = [MetaDemandStruct(**out) for out in data["meta"]]
    inputs = [
        InputStruct(
            **{k if k != "from" else "input_from": v for k, v in inp.items()}
        )
        for inp in data["inputs"]
    ]

    metaModel = MetaStruct(
        name=data["name"],
        id=data["id"],
        short_name=data["short_name"],
        category=data["type"],
        description=data["description"],
        version=data["version"],
        debug=data["debug"],
        constants=constants,
        inputs=inputs,
        outcome=outcome,
        outputs=outputs,
        demands=demands,
        meta=meta_demands,
    )

    return metaModel
