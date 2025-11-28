"""types definition"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BaseStruct:
    """Base structure that aggregates common attributes.

    Attributes:
        name (str): The name of the item
        description (str): A description of the item.
        units (str): Measurement units associated with the item.
    """

    name: str
    description: str
    units: str


@dataclass
class ConstantStruct(BaseStruct):
    """Structure for constants used in the model.

    Attributes:
        citation (str): Citation
        source (str): Source from which the constant is derived.
        value (float): The constant value.
        range (Optional[list[float]]): Optional range of valid values for the constant.
    """

    citation: str
    source: str
    value: float
    range: Optional[list[float]] = None


@dataclass
class OutcomeStruct(BaseStruct):
    """Structure for outcomes in the model.

    Attributes:
        same_result (str): The expected outcome description.
        range (Optional[list[float]]): Optional range of values for the outcome.
        tests (Optional[list[float]]): Optional tests associated with the outcome.
    """

    same_result: str
    range: Optional[list[float]] = None
    tests: Optional[list[float]] = None


@dataclass
class ItemStruct(BaseStruct):
    """Structure for items used in demand, meta-demand, and output.

    Attributes:
        args (list[dict[str, Any]]): Arguments associated with the item.
        operation (str): The operation to be performed on the item.
        tests (Optional[list[float]]): Optional tests associated with the item.
    """

    args: list[dict[str, Any]]
    operation: str
    tests: Optional[list[float]] = None


@dataclass(kw_only=True)
class DemandStruct(ItemStruct):
    """Structure for demands in the model.

    Attributes:
        used (str): The process that is using the demand.
        meta (Optional[str]): Optional metadata associated with the demand.
    """

    used: str
    meta: Optional[str] = None


@dataclass
class MetaDemandStruct(ItemStruct):
    """Structure for meta-demands in the model.

    This inherits from ItemStruct.
    """


@dataclass
class InputStruct(BaseStruct):
    """Structure for inputs in the model.

    Attributes:
        value (list[float]): List of input values.
        input_from (str): The source of the input, using 'from' as a JSON key.
        range (Optional[list[float]]): Optional range of valid values for the input.
    """

    value: list[float]
    input_from: str = field(metadata={"json_key": "from"})
    range: Optional[list[float]] = None


@dataclass
class OutputStruct(ItemStruct):
    """Structure for outputs in the model.

    Attributes:
        value (Optional[float]): Optional output value.
        range (Optional[list[float]]): Optional range of valid values for the output.
    """

    value: Optional[float] = None
    range: Optional[list[float]] = None


@dataclass
class ModelStruct:  # pylint: disable=too-many-instance-attributes
    """Structure for the model configuration.

    Attributes:
        name (str): The name of the model.
        short_name (str): A short name for the model.
        id (str): Unique identifier for the model.
        category (str): The category of the model.
        description (str): A description of the model.
        version (str): Version information for the model.
        debug (str): Debugging information.
        constants (list[ConstantStruct]): List of constants used in the model.
        inputs (list[InputStruct]): List of inputs for the model.
        outputs (list[OutputStruct]): List of outputs for the model.
    """

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
    """Structure for meta models.

    Attributes:
        outcome (OutcomeStruct): The expected outcome of the model.
        demands (list[DemandStruct]): List of demands associated with the model.
        meta (list[MetaDemandStruct]): List of meta-demands associated with the model.
    """

    outcome: OutcomeStruct
    demands: list[DemandStruct]
    meta: list[MetaDemandStruct]


def json_to_model_struct(data: dict[str, Any]) -> ModelStruct:
    """Parse the JSON object and transform it into a ModelStruct object.

    This function takes a JSON dictionary representation of a model and
    constructs a ModelStruct object, extracting the necessary fields.

    Args:
        data (dict[str, Any]): JSON data representing the model. Must include
            'constants', 'inputs', 'outputs', and other required attributes.

    Returns:
        ModelStruct: An instance of ModelStruct filled with the parsed data.

    Example:
        model_struct = json_to_model_struct(json_data)
    """
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
    """Parse the JSON object and transform it into a MetaStruct object.

    This function takes a JSON dictionary representation of a meta model and
    constructs a MetaStruct object, extracting all necessary fields, including
    constants, inputs, and outputs.

    Args:
        data (dict[str, Any]): JSON data representing the meta model. Must include
            'constants', 'outcome', 'inputs', 'outputs', 'demands', and other required attributes.

    Returns:
        MetaStruct: An instance of MetaStruct filled with the parsed data.

    Example:
        meta_struct = json_to_meta_struct(json_meta_data)
    """
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
