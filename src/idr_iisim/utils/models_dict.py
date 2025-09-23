"""Industry"""

import json
from typing import Any, Optional

import yaml

from idr_iisim.models.meta import Meta
from idr_iisim.models.process import Process
from idr_iisim.templates import load_template


class Industry:
    """Industry class"""

    def __init__(self, meta: Optional[Meta] = None):
        # initializes an object of the class with an empty models dictionary.
        self.models: dict[str, Process] = {}
        self.dependencies: dict[str, set[str]] = {}
        self.processed_models: dict[str, bool] = {}
        self.meta: Optional[Meta] = meta

    def add_process(self, key: str, process: Process) -> None:
        """add model to the industry"""
        self.models[key] = process
        self.processed_models[key] = False

        # add dependencies
        # model_id -> list[dependent_models_ids]
        model_dependencies = list(
            filter(lambda x: x.input_from is not None, process.config.inputs)
        )

        # filter from values
        from_list = set(map(lambda x: x.input_from, model_dependencies))
        if len(from_list) > 0:
            self.dependencies[key] = from_list

    def set_meta(self, meta: Meta) -> None:
        """set or update the meta of this industry"""
        self.meta = meta

    def check_types(self) -> None:
        """check types among processes"""
        assert self.meta is not None
        inputs_checks = [(self.meta.config.name, self.meta.config.inputs)]
        inputs_checks += [
            (name, model.config.inputs) for name, model in self.models.items()
        ]
        for name, inputs in inputs_checks:
            for input_field in inputs:
                # Check if units are the same in both processess
                if input_field.input_from is not None:
                    model_from = self.models[input_field.input_from]
                    if input_field.name not in model_from.outputs:
                        raise ValueError(
                            f"'{input_field.name}' does not exist in "
                            + f"'{model_from.config.name}'"
                        )
                    units_from = model_from.outputs[input_field.name].units
                    if units_from != input_field.units:
                        raise ValueError(
                            f"Unit for '{input_field.name}' differs in "
                            + f"'{name}' ({input_field.units}) and "
                            + f"'{model_from.config.name}' ({units_from})"
                        )
        for demand in self.meta.demands.values():
            model_from = self.models[demand.used]
            if demand.name not in model_from.inputs:
                raise ValueError(
                    f"'{demand.name}' does not exist in "
                    + f"'{model_from.config.name}'"
                )
            units_from = model_from.inputs[demand.name].units
            if units_from != demand.units:
                raise ValueError(
                    f"Unit for '{demand.name}' differs in "
                    + f"'Meta' ({demand.units}) and "
                    + f"'{model_from.config.name}' ({units_from})"
                )

    def generate_execution_queue(self) -> list[str]:
        """Generate the correct execution queue of the processes"""
        queue: list[str] = []

        # Include processes without dependencies
        for process in self.models:
            if process not in self.dependencies:
                queue.append(process)

        # Add the rest of the processes once their dependencies are fullfilled
        while len(queue) != len(self.models):
            for process, dependencies in self.dependencies.items():
                if process not in queue:
                    should_include_process = True
                    for dependency in dependencies:
                        if dependency not in queue:
                            should_include_process = False
                            break
                    if should_include_process:
                        queue.append(process)

        return queue

    def script_generator(self) -> str:
        """Generator of the script"""
        assert self.meta is not None
        # Load the template content
        template_path = "templates/template_generated_industrial_class.txt"
        method_template = load_template(template_path)

        args = "self"
        constructor = ""
        constants = []
        process_methods = []
        min_units = 5
        max_units = 1000
        units = self.meta.get_units()

        constants.append(self.meta.constants_generator())

        for model_name in self.generate_execution_queue():
            model = self.models[model_name]
            process_methods.append(model.process_methods_generator())
            constants.append(model.constants_generator())
            constructor += self.meta.constructor_pre_generator(model.config.id)
            constructor += model.process_call_method_generator()
            constructor += "\n        "

        constructor += self.meta.constructor_post_generator()

        outcome_name = self.meta.config.outcome.name
        args += ", " + outcome_name

        return method_template.substitute(
            name=self.meta.config.short_name,
            fullname=f'"{self.meta.config.name}"',
            description=self.meta.config.description,
            outcome_name=outcome_name,
            constructor_method=constructor,
            constants="\n".join(constants),
            args=args,
            process_methods="\n".join(process_methods),
            get_methods=self.meta.getters_generator(),
            units=json.dumps(units, indent=4),
            min_units=min_units,
            max_units=max_units,
        )


def load_yaml(path: str) -> dict[str, Any]:
    """load industry's yaml file"""
    try:
        with open(path, encoding="utf-8") as file:
            data: dict[str, Any] = yaml.safe_load(file)
            return data
    except Exception as e:
        raise e
