import yaml
from src.exception import ModelException
from src.logger import logging
import sys,os

def write_yaml_file(file_path:str, content: object, replace:bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise ModelException(e,sys)