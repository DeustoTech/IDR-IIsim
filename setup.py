import importlib
import os

from idr_iisim.models.model import Model
from idr_iisim.utils.config import GlobalVariables
from idr_iisim.utils.execution import generate_execution_queue
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.models_dict import models_dict
from idr_iisim.utils.types import ArgumentStruct

class_name = "MethodModel"


def find_processes() -> None:
    path = os.path.dirname(os.path.realpath(__file__)) + "/idr_iisim/industry"
    for root, dirs, files in os.walk(path, topdown=False):
        if "model.py" in files:
            model_path = os.path.join(root, "model.py")
            spec = importlib.util.spec_from_file_location(class_name, model_path)
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)
            instance: Model = getattr(module, class_name)()

            # save instance in ModelDict class
            key = instance.config.id
            models_dict.add_model(key=key, model=instance)

    models_dict.set_dict_to_loaded()
    return None


def init() -> None:
    i_logger.logger.info("starting iDesignRES tool")

    # read config file
    i_logger.logger.debug("reading config file")
    GlobalVariables()
    i_logger.logger.debug("config file read")

    # find processes
    i_logger.logger.debug("finding processes")
    find_processes()
    i_logger.logger.debug("processes found")

    return None


def main() -> None:
    init()
    i_logger.logger.info("iDesignRES tool started")

    all_dependencies = models_dict.dependencies
    for key, value in models_dict.models.items():
        queue = generate_execution_queue(key)

        # perform calculations for each model in the queue so that the dependencies are met
        for model_instance_id in queue:
            print(f"Calculating model: {model_instance_id}")
            instance = models_dict.models[model_instance_id]

            # check whether the model in the queue has any dependencies
            if model_instance_id in all_dependencies:
                # if there are dependencies, then check whether they are already calculated
                dependencies = all_dependencies[model_instance_id]
                for dependency in dependencies:
                    # if calculated, then get the results
                    output_dependency = models_dict.models[dependency].results
                    instance.prepare_calculation(dependency, output_dependency)

            if models_dict.is_model_processed(model_instance_id):
                continue

            # calculate the model
            instance.calculate()
            models_dict.mark_model_as_processed(model_instance_id)
            print("\n\n")


print("\n")

i_logger.logger.info("iDesignRES tool finished")
pass

if __name__ == "__main__":
    main()
