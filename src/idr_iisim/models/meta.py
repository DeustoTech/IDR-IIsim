"""Module to process the meta.yaml, the industry's configuration"""

from typing import Any

from idr_iisim.models.model import Model
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.structs import (
    DemandStruct,
    ItemStruct,
    MetaDemandStruct,
    MetaStruct,
    OutcomeStruct,
    json_to_meta_struct,
)


class Meta(Model):
    """Meta class to handle parsing and managing meta data configurations.

    Attributes:
        outcome (dict[str, OutcomeStruct]): A dictionary holding outcomes.
        demands (dict[str, DemandStruct]): A dictionary holding demands.
        meta_demands (dict[str, MetaDemandStruct]): A dictionary holding meta-demands.
        config (MetaStruct): Parsed configuration data.
    """

    def __init__(self, yaml_data: dict[str, Any], path: str):
        """Initialize Meta class with YAML data and the path.

        Args:
            yaml_data (dict[str, Any]): Parsed YAML configuration data.
            path (str): Path to the configuration file.
        """
        super().__init__(path)
        self.outcome: dict[str, OutcomeStruct] = {}
        self.demands: dict[str, DemandStruct] = {}
        self.meta_demands: dict[str, MetaDemandStruct] = {}

        # Parse data
        i_logger.debug("parsing %s", yaml_data["name"])
        self.config: MetaStruct = json_to_meta_struct(yaml_data)

        items: list[ItemStruct] = [
            d for d in self.config.demands if d.meta is None
        ]
        items += list(self.config.meta)
        items += list(self.config.outputs)

        self.process_config(items, self.config)
        # Parse demands
        for demand in self.config.demands:
            self.demands[demand.name] = demand
        # Parse meta demands
        for meta_demand in self.config.meta:
            self.meta_demands[meta_demand.name] = meta_demand
        # Parse outcome
        self.outcome[self.config.outcome.name] = self.config.outcome

    def get_getter_items(self) -> list[tuple[str, str]]:
        """Generate a list of item descriptions for getter configuration.

        Returns:
            list[tuple[str, str]]: A list of tuples containing variable
            names and their descriptions.
        """
        getter_items = []
        # Outcome
        for variable_name, output in self.outcome.items():
            getter_items.append((variable_name, output.description))

        # outputs
        for variable_name, item in self.functions_map.items():
            getter_items.append((variable_name, item["description"]))

        return getter_items

    def constructor_pre_generator(self, process: str) -> str:
        """Generate initialization code for demands used in a specified process.

        Args:
            process (str): The name of the process for which initializations are generated.

        Returns:
            str: The generated initialization code as a string.
        """
        items: list[tuple[str, ItemStruct]] = []
        for variable_name, values in self.demands.items():
            if values.used == process:
                items.append((variable_name, values))

        process_methods = _process_items(items)
        return "\n        ".join(process_methods)

    def constructor_post_generator(self) -> str:
        """Generate initialization code for meta-demands and outputs.

        Returns:
            str: The generated initialization code as a string.
        """

        # Meta demands
        items: list[tuple[str, ItemStruct]] = list(self.meta_demands.items())
        # Outputs
        items.extend(list(self.outputs.items()))
        # Process items
        process_methods = _process_items(items)

        return "\n        ".join(process_methods)

    def get_units(self) -> dict[str, str]:
        """Get the units of demands and outputs.

        Returns:
            dict[str, str]: A dictionary mapping variable names to their units.
        """
        units = {}

        # Outcome
        for outcome_value in self.outcome.values():
            units[outcome_value.name] = outcome_value.units
        # Demands
        for demand_value in self.demands.values():
            if demand_value.meta is None:
                units[demand_value.name] = demand_value.units
        # Meta-demands
        for meta_demand_value in self.meta_demands.values():
            units[meta_demand_value.name] = meta_demand_value.units
        # Outputs
        for output_value in self.outputs.values():
            units[output_value.name] = output_value.units

        return units


def _process_items(items: list[tuple[str, ItemStruct]]) -> list[str]:
    process_methods = []
    # Process items
    for variable_name, values in items:
        expression = values.operation
        for arg in values.args:
            if arg["type"] != "constants":
                expression = expression.replace(
                    arg["name"], f"self.__{arg['name']}"
                )
        method_script = f"self.__{variable_name} = {expression}"
        process_methods += [method_script]
    return process_methods
