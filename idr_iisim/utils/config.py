__package__ = "utils"

import json
import os
from dataclasses import dataclass
import yaml
from idr_iisim.utils.logger import i_logger
from dotenv import load_dotenv  # Import dotenv


@dataclass
class Config:
    foo: str = "default_foo"


class GlobalVariables:
    config_path                  : str
    templates_path               : str
    template_generated_script    : str
    generated_method_script_name : str
    config: Config

    def __init__(self) -> None:
        # self.config_path = os.environ.get("CONFIG_PATH", "/home/ivan/Desktop/IDR/IDR-IIsim/config")
        self.config_path    = os.environ.get("CONFIG_PATH")
        self.templates_path = os.environ.get("TEMPLATES_PATH")  
        self.template_generated_script_filename = os.environ.get("TEMPLATE_GENERATED_SCRIPT_FIELNAME") 
        self.generated_method_script_name       = os.environ.get("GENERATED_METHOD_SCRIPT_FILENAME")
        
        
        # read config file
        try:
            config_file: str = self.config_path + "/config.yaml"
            with open(config_file) as file:
                data: dict = yaml.safe_load(file)
            self.config = Config(**data)
        except Exception as e:
            i_logger.logger.error("failed to read config file: " + str(e))
            raise e
    
    
    def __str__(self):
        return f"config_path: {self.config_path}, templates_path: {self.templates_path}, template_generated_script: {self.template_generated_script_filename}"   
        
        

# Reload the .env file every time this script is run
load_dotenv()
global_variables = GlobalVariables()
