import json
import yaml
from idr_iisim.models.model import Model
from idr_iisim.models.meta import Meta
from string import Template  # Use Template for substitution
from idr_iisim.utils.logger import i_logger
from typing import Optional


class Industry:
    def __init__(self, meta: Optional[Meta] = None):
        # initializes an object of the class with an empty models dictionary.
        self.models: dict[
            str, Model
        ] = {}  # model_id -> Model,  models maps unique model IDs to their respective instances.
        self.dependencies: dict[str, set[str]] = {}
        self.loaded: bool = False
        self.processed_models: dict[str, bool] = {}
        self.meta: Optional[Meta] = meta

    def add_model(self, key: str, model: Model):
        self.models[key] = model
        self.processed_models[key] = False

        # add dependencies
        # model_id -> list[dependent_models_ids]
        model_dependencies = list(
            filter(lambda x: x.input_from is not None, model.config.inputs)
        )

        # filter from values
        from_list = set(map(lambda x: x.input_from, model_dependencies))
        if len(from_list) > 0:
            self.dependencies[key] = from_list

    def set_meta(self, meta: Meta) -> None:
        self.meta = meta

    def set_dict_to_loaded(self):
        self.loaded = True

    def mark_model_as_processed(self, model_id) -> None:
        self.processed_models[model_id] = True

    def is_model_processed(self, model_id) -> bool:
        return self.processed_models[model_id]

    def get_model(self, key: str) -> Model:
        return self.models[key]

    def check_types(self) -> None:
        assert self.meta is not None
        inputs_checks = [(self.meta.config.name, self.meta.config.inputs)]
        inputs_checks += [
            (name, model.config.inputs) for name, model in self.models.items()
        ]
        for name, inputs in inputs_checks:
            for input in inputs:
                # Check if units are the same in both processess
                if input.input_from is not None:
                    model_from = self.models[input.input_from]
                    if input.name not in model_from.outputs:
                        raise ValueError(
                            f"'{input.name}' does not exist in "
                            + f"'{model_from.config.name}'"
                        )
                    units_from = model_from.outputs[input.name].units
                    if units_from != input.units:
                        raise ValueError(
                            f"Unit for '{input.name}' differs in "
                            + f"'{name}' ({input.units}) and "
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

    def generate_execution_queue(self):
        queue: list[str] = []

        # Include processes without dependencies
        for process in self.models:
            if process not in self.dependencies:
                queue.append(process)

        # Add the rest of the processes once their dependencies are fullfilled
        while len(queue) != len(self.models):
            for process in self.dependencies:
                if process not in queue:
                    should_include_process = True
                    for dependency in self.dependencies[process]:
                        if dependency not in queue:
                            should_include_process = False
                            break
                    if should_include_process:
                        queue.append(process)

        return queue

    def script_generator(self) -> str:
        assert self.meta is not None
        # Load the template content
        template_path = "templates/template_generated_industrial_class.txt"
        try:
            with open(template_path, "r") as template_file:
                template_content = template_file.read()
        except FileNotFoundError:
            i_logger.logger.error(f"Template file not found: {template_path}")
            raise
        except Exception as e:
            i_logger.logger.error(f"Error reading template file: {e}")
            raise

        method_template = Template(template_content)
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


def load_yaml(path: str) -> dict:
    try:
        with open(path) as file:
            data: dict = yaml.safe_load(file)
            return data
    except Exception as e:
        raise e


models_dict = Industry()
