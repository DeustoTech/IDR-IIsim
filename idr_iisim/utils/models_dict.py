from idr_iisim.models.model import Model


class ModelDict:
    models: dict[str, Model]
    dependencies: dict[str, list[str]] = {}
    loaded: bool = False
    processed_models: dict[str, bool] = {}

    def __init__(self):
        self.models = {}
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
