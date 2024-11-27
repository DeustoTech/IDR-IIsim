__package__ = "utils"

import json
import os
from dataclasses import dataclass
import yaml
from idr_iisim.utils.logger import i_logger
from dotenv import load_dotenv, dotenv_values


@dataclass
class Config:
    foo: str = "default_foo"


class GlobalVariables:
    config_path    : str
    templates_path : str
    industries_path: str
    template_generated_script_filename : str
    generated_model_script_filename    : str
    config: Config

    def __init__(self) -> None:
        # Clear existing environment variables defined in the .env file
        for key in dotenv_values(".env").keys():
            os.environ.pop(key, None)
        
        # Reload the .env file
        load_dotenv(".env", override=True)
    
        # self.config_path = os.environ.get("CONFIG_PATH", "/home/ivan/Desktop/IDR/IDR-IIsim/config")
        self.config_path     = os.environ.get("CONFIG_PATH")
        self.templates_path  = os.environ.get("TEMPLATES_PATH")  
        self.industries_path = os.environ.get("INDUSTRIES_PATH")
        self.template_generated_script_filename = os.environ.get("TEMPLATE_GENERATED_SCRIPT_FILENAME") 
        self.generated_model_script_filename    = os.environ.get("GENERATED_MODEL_SCRIPT_FILENAME")
        
        
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
        return f"config_path: {self.config_path}, templates_path: {self.templates_path}, industries_path: {self.industries_path}. template_generated_script: {self.template_generated_script_filename}, generated_model_script: {self.generated_model_script_filename}"   
        
        

# Reload the .env file every time this script is run
load_dotenv()
global_variables = GlobalVariables()
