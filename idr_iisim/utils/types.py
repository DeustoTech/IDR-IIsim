__package__ = "utils"

from dataclasses import dataclass, field


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
    input_from: str = field(metadata={"json_key": "from"})
    units: str


@dataclass
class OutputStruct:
    name: str
    label: str
    description: str
    operation: str
    args: list[str]
    units: str
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
