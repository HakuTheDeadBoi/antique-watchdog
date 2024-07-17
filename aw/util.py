import json
import os

from aw.constraint import Constraint
from aw.error import CloseThreadError
from aw.query import Query

from aw import ROOT_DIR, CONFIG_FILE, QUERIES_FILE

# maybe change name to load_config
def config_loader(key_list: list[str]) -> dict[str]:
    """
    Loads configuration values from a JSON file for the specified keys.

    This function opens and reads a JSON file specified by CONFIG_FILE located 
    at ROOT_DIR. It then extracts the values for the provided keys in key_list.

    Args:
        key_list (list[str]): A list of keys for which values need to be retrieved 
                              from the configuration file.

    Returns:
        dict[str]: A dictionary with keys from key_list and their corresponding 
                   values from the JSON file. If a key is not found, its value will be None.

    Raises:
        CloseThreadError: If there is an issue reading the file or decoding the JSON content.
    """
    config_dict = {}
    json_data = None

    try:
        with open(os.path.join(ROOT_DIR, CONFIG_FILE), "r", encoding="utf-8") as FILE:
            json_data = json.load(FILE)
    except json.JSONDecodeError as e:
        raise CloseThreadError(f"JSON parsed unsuccessfully: {e}") 
    except IOError as e:
        raise CloseThreadError(f"Problem reading file: {e}")

    for key in key_list:
        value = json_data.get(key)
        config_dict.update({key: value})

    return config_dict

def load_queries() -> list[Query]:
    with open(os.path.join(ROOT_DIR, QUERIES_FILE), "r", encoding="utf-8") as FILE:
        data = json.load(FILE)

    query_list = []

    for query_data in data.get("queries"):
        constraint_list = []

        for constraint_data in query_data.get("constraint_list"):
            constraint = Constraint(
                key = constraint_data.get("key"),
                value = constraint_data.get("value"),
                relation = constraint_data.get("relation"),
                asciize = constraint_data.get("asciize")
            )
            constraint_list.append(constraint)
                    
        query = Query(
            query_string = query_data.get("query_string"),
            constraint_list = constraint_list,
            asciize = query_data.get("asciize")
        )

        query_list.append(query)

    return query_list