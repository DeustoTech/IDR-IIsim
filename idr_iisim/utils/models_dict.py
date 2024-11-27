from idr_iisim.models.model import Model


class ModelDict:
    models          : dict[str, Model]              # model_id -> Model,  models maps unique model IDs to their respective instances.
    dependencies    : dict[str, list[str]] = {}     # model_id -> list[dependent_models_ids],  dependencies maps model IDs to the IDs of models they depend on.
    loaded          : bool = False                  # flag to check if the models have been loaded
    processed_models: dict[str, bool] = {}          # model_id -> bool,  processed_models tracks whether each model has been processed.

    def __init__(self):
        # initializes an object of the class with an empty models dictionary.
        self.models = {}        # model_id -> Model,  models maps unique model IDs to their respective instances.
        pass

    def add_model(self, key: str, model: Model):
        self.models[key] = model
        self.processed_models[key] = False

        # add dependencies
        # model_id -> list[dependent_models_ids]
        model_dependencies = list(filter(lambda x: x["from"] is not None, model.config.inputs))

        # filter from values
        from_list = list(map(lambda x: x["from"], model_dependencies))
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


models_dict = ModelDict()
