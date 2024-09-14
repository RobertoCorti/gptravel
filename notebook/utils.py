import json
import os
import warnings
from pathlib import Path
from typing import Any, Dict, List

from gptravel.core.utils.regex_tool import JsonExtractor


def check_env_variable(env_variable: str) -> None:
    value = os.getenv(env_variable)
    if value is not None:
        print(f"{env_variable} loaded correctly")
    else:
        warnings.warn(f"{env_variable} not loaed")


def check_file_exists(file_path: str) -> bool:
    try:
        my_abs_path = Path(file_path).resolve(strict=True)
    except FileNotFoundError:
        return False
    return True


def generate_tp_name(parameters: Dict[str, Any]) -> str:
    return (
        "tp_dep_"
        + parameters["departure_place"]
        + "_arr_"
        + parameters["destination_place"]
        + "_n_d"
        + str(parameters["n_travel_days"])
    )


def from_json_to_text(text: str) -> Dict[Any, Any]:
    regex = JsonExtractor()
    dict_string = regex(text)[0]
    try:
        json_object = json.loads(dict_string)
    except json.decoder.JSONDecodeError:
        json_object = json.loads(r"{}".format(dict_string[0].replace("'", '"')))
    return json_object


def build_travel_plan_object(_dict):
    return TravelPlanJSON(
        departure_place=_dict["departure_place"],
        destination_place=_dict["destination_place"],
        n_days=_dict["n_travel_days"],
        travel_plan_json=_dict["travel_plan_json_str"],
        json_keys_depth_map={"city": 1, "day": 0},
    )
