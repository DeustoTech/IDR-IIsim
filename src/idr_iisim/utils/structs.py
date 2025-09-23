"""types definition"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BaseStruct:
    """Base Struct: it aggregates the common attributes"""

    name: str
    description: str
    units: str


@dataclass
class ConstantStruct(BaseStruct):
    """Constant Struct"""

    citation: str
    source: str
    value: float
    range: Optional[list[float]] = None


@dataclass
class OutcomeStruct(BaseStruct):
    """Outcome Struct"""

    same_result: str


@dataclass
class ItemStruct(BaseStruct):
    """Item Struct: it aggregates the attributes used in Demand, Meta-Demand and Output"""

    args: list[dict[str, Any]]
    operation: str


@dataclass
class DemandStruct(ItemStruct):
    """Demand Struct"""

    used: str
    meta: Optional[str] = None


@dataclass
class MetaDemandStruct(ItemStruct):
    """Meta-Demand Struct"""


@dataclass
class InputStruct(BaseStruct):
    """Input Struct"""

    value: list[float]
    input_from: str = field(metadata={"json_key": "from"})
    range: Optional[list[float]] = None


@dataclass
class OutputStruct(ItemStruct):
    """Output Struct"""

    value: Optional[float] = None
    range: Optional[list[float]] = None


@dataclass
class ModelStruct:  # pylint: disable=too-many-instance-attributes
    """Model Struct"""

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
class MetaStruct(ModelStruct):
    """Meta Struct"""

    outcome: OutcomeStruct
    demands: list[DemandStruct]
    meta: list[MetaDemandStruct]


def json_to_model_struct(data: dict[str, Any]) -> ModelStruct:
    """Parse the JSON object and transform it to the model struct object"""
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


def json_to_meta_struct(data: dict[str, Any]) -> MetaStruct:
    """Parse the JSON object and transform it to the Meta struct object"""
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

    meta_model = MetaStruct(
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

    return meta_model
