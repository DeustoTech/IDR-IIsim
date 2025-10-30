"""IDR-IISIM Compiler main"""

import os
import traceback
from pathlib import Path

from dotenv import load_dotenv

from idr_iisim.models.meta import Meta
from idr_iisim.models.process import Process
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.models_dict import Industry, load_yaml
from idr_iisim.utils.schema import Validator


def process_industry(name: str, industry_path: str) -> None:
    """Process and generate code for a specified industry.

    This function validates and processes all YAML files in the given industry path,
    generating a Python script for the industry based on the loaded configurations.

    Args:
        name (str): The name of the industry to be processed.
        industry_path (str): The path where the YAML files of the industry are stored.

    Raises:
        Exception: If there are issues in processing the industry files.
    """
    i_logger.info("Processing industry: %s", name)
    industry = Industry()
    yaml_validator = Validator()

    for file in Path(industry_path).rglob("*.yaml"):
        yaml_path = str(file)
        yaml_data = load_yaml(yaml_path)
        yaml_validator.validate(yaml_data)
        if yaml_data["type"] == "industry":
            meta = Meta(yaml_data, yaml_path)
            industry.set_meta(meta)
        else:
            process = Process(yaml_data, yaml_path)
            # save instance in ModelDict class
            key = process.config.id
            industry.add_process(key=key, process=process)

    # Check types
    industry.check_types()
    assert industry.meta is not None

    industries_final_path = "industries"
    result_path = os.path.join(
        industries_final_path,
        f"{industry.meta.config.short_name.lower()}.py",
    )

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(industry.script_generator())

    i_logger.info("Industry '%s' processed.", name)


def main() -> None:
    """Main program entry point.

    The program iterates over all industries found in the specified source folder,
    processing each industry to generate its corresponding model.

    Raises:
        Exception: If there is an error during the processing of the industries.
    """
    try:
        i_logger.info("starting iDesignRES tool")
        industries_path = os.environ.get("INDUSTRIES_PATH", "Sources")
        for elem in os.listdir(industries_path):
            elem_path = os.path.join(industries_path, elem)
            if os.path.isdir(elem_path):
                process_industry(elem, elem_path)
        i_logger.info("iDesignRES tool finished")
    except Exception as err:  # pylint: disable=broad-exception-caught
        print()
        traceback.print_exc()
        i_logger.error(err)
        i_logger.info("iDesignRES tool finished UNSUCCESFULLY")


if __name__ == "__main__":
    #
    os.system("cls" if os.name == "nt" else "clear")
    load_dotenv()
    main()
