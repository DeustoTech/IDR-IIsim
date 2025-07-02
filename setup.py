import importlib
import os

from idr_iisim.models.model import Model  # import Model class
from idr_iisim.utils.config import (
    GlobalVariables,
)  # read config file and set global variables
from idr_iisim.utils.execution import generate_execution_queue
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.models_dict import models_dict
from idr_iisim.utils.schema import Validator

# class name of the model
class_name = "MethodModel"


def find_processes() -> None:
    """Find all processes in the industry folder and load them into the models_dict"""
    # path = os.path.dirname(os.path.realpath(__file__)) + "/idr_iisim/industry"

    # get env var INDUSTRY_PATH & set the path
    path = os.environ.get("INDUSTRIES_PATH")

    # walk through the industry folder: generating the file names in a directory tree by walking the directory tree either top-down or bottom-up
    # Uses os.walk to traverse the directory tree starting from path.
    for root, dirs, files in os.walk(
        path, topdown=False
    ):  # root: The current directory path, dirs: List of subdirectories, files: List of files in the current directory.
        # check if the folder contains a model.py file
        if "model.py" in files:
            # Dynamically loads the model.py file as a Python module:
            # loads these modules, creates instances of a specific class (class_name) within each model.py
            model_path = os.path.join(root, "model.py")
            spec = importlib.util.spec_from_file_location(
                class_name, model_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # execute the module

            # create an instance of the class
            instance: Model = getattr(module, class_name)()

            # save instance in ModelDict class
            key = instance.config.id
            models_dict.add_model(key=key, model=instance)

        # log the key directory of the instance
        i_logger.logger.debug(f"instance: {root}")

    # set the loaded flag to True
    models_dict.set_dict_to_loaded()
    # size of the models dictionary: number of models in the dictionary
    i_logger.logger.debug(f"models_dict: {models_dict.models}")
    return None


def init() -> None:
    i_logger.logger.info("starting iDesignRES tool\n")

    # read config file
    i_logger.logger.debug("reading config file")
    GlobalVariables()
    i_logger.logger.debug("env paths: " + GlobalVariables().__str__())
    i_logger.logger.debug("config file read and global variables set\n")

    # init yaml validator
    i_logger.logger.debug("initializing yaml validator")
    Validator()
    # i_logger.logger.debug("schema: " + str(Validator().validator))
    i_logger.logger.debug(
        "yaml validator initialized (based on a schema.yaml)\n"
    )

    # find processes
    i_logger.logger.debug("finding processes")
    find_processes()
    i_logger.logger.debug(f"methods found: {str(models_dict.models.keys())}\n")

    return None


def main() -> None:
    init()
    i_logger.logger.info("iDesignRES tool started")

    all_dependencies = models_dict.dependencies
    print(all_dependencies)
    # for key in sorted(models_dict.models):
    for model_instance_id in generate_execution_queue(
        list(models_dict.models.keys()), all_dependencies
    ):
        print(f"Calculating model: {model_instance_id}")
        instance = models_dict.models[model_instance_id]

        # check whether the model in the queue has any dependencies
        if model_instance_id in all_dependencies:
            # if there are dependencies, then check whether they are already calculated
            dependencies = all_dependencies[model_instance_id]
            i_logger.logger.debug(
                f"checking model dependencies: {dependencies}"
            )
            for dependency in dependencies:
                # if calculated, then get the results
                output_dependency = models_dict.models[dependency].results
                instance.prepare_calculation(dependency, output_dependency)

        # calculate the model
        instance.calculate()
        models_dict.mark_model_as_processed(model_instance_id)

        # print diagrams
        instance.print_diagram()
        print("\n\n")

        # log input and results
        i_logger.logger.debug(f"external inputs: {instance.external_inputs}")
        i_logger.logger.debug(f"results: {instance.results}")

        # call script_generator
        instance.script_generator(
            GlobalVariables().templates_path
            + GlobalVariables().template_generated_script_filename,
            GlobalVariables().generated_model_script_filename,
        )

    print("\n")
    i_logger.logger.info("iDesignRES tool finished")


if __name__ == "__main__":
    #
    os.system("cls" if os.name == "nt" else "clear")
    main()
