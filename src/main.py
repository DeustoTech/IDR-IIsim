import os
from pathlib import Path
import traceback

from idr_iisim.utils.models_dict import Industry, load_yaml
from idr_iisim.models.model import Model  # import Model class
from idr_iisim.models.meta import Meta  # import Model class
from idr_iisim.utils.logger import i_logger


def process_industry(name: str, industry_path: str) -> None:
    """Process the industry"""
    i_logger.logger.info(f"Processing industry: {name}")
    industry = Industry()

    for file in Path(industry_path).rglob("*.yaml"):
        yaml_path = str(file)
        yaml_data = load_yaml(yaml_path)
        if yaml_data["type"] == "industry":
            meta = Meta(yaml_data, yaml_path)
            industry.set_meta(meta)
        else:
            model = Model(yaml_data, yaml_path)
            # save instance in ModelDict class
            key = model.config.id
            industry.add_model(key=key, model=model)

    # Check types
    industry.check_types()
    assert industry.meta is not None

    industries_final_path = "industries"
    with open(
        os.path.join(
            industries_final_path,
            f"{industry.meta.config.short_name.lower()}.py",
        ),
        "w",
    ) as f:
        f.write(industry.script_generator())

    i_logger.logger.info(f"Industry '{name}' processed.")


def main() -> None:
    try:
        i_logger.logger.info("starting iDesignRES tool")
        # industries_path = os.environ.get("INDUSTRIES_PATH", "")
        industries_path = "Sources"
        for elem in os.listdir(industries_path):
            elem_path = os.path.join(industries_path, elem)
            if os.path.isdir(elem_path):
                process_industry(elem, elem_path)
        i_logger.logger.info("iDesignRES tool finished")
    except Exception as err:
        print()
        traceback.print_exc()
        i_logger.logger.error(err)
        i_logger.logger.info("iDesignRES tool finished UNSUCCESFULLY")


if __name__ == "__main__":
    #
    os.system("cls" if os.name == "nt" else "clear")
    main()
