import json
import os

from aw.error import CloseThreadError
from aw import ROOT_DIR, CONFIG_FILE

def config_loader(key_list: list[str]) -> dict[str]:
    config_dict = {}
    json_data = None

    try:
        with open(os.path.join(ROOT_DIR, CONFIG_FILE), "r") as FILE:
            json_data = json.load(FILE)
    except json.JSONDecodeError as e:
            raise CloseThreadError(f"JSON parsed unsuccessfully: {e}") 
    except IOError as e:
        raise CloseThreadError(f"Problem reading file: {e}")

    for key in key_list:
        value = json_data.get(key)
        config_dict.update({key: value})

    return config_dict