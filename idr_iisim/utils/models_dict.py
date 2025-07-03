from idr_iisim.models.model import Model


class ModelDict:
    models: dict[
        str, Model
    ]  # model_id -> Model,  models maps unique model IDs to their respective instances.
    dependencies: dict[
        str, set[str]
    ] = {}  # model_id -> list[dependent_models_ids],  dependencies maps model IDs to the IDs of models they depend on.
    loaded: bool = False  # flag to check if the models have been loaded
    processed_models: dict[
        str, bool
    ] = {}  # model_id -> bool,  processed_models tracks whether each model has been processed.

    def __init__(self):
        # initializes an object of the class with an empty models dictionary.
        self.models = {}  # model_id -> Model,  models maps unique model IDs to their respective instances.
        pass

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
        pass

    def set_dict_to_loaded(self):
        self.loaded = True
        pass

    def mark_model_as_processed(self, model_id) -> None:
        self.processed_models[model_id] = True
        pass

    def is_model_processed(self, model_id) -> bool:
        return self.processed_models[model_id]

    def get_model(self, key: str) -> Model:
        return self.models[key]

    def check_types(self) -> None:
        for model in self.models.values():
            for input in model.config.inputs:
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
                            + f"'{model.config.name}' ({input.units}) and "
                            + f"'{model_from.config.name}' ({units_from})"
                        )


models_dict = ModelDict()
