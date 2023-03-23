from typing import Any, Dict, List


def extract_keys_by_depth_from_json(json_obj: Dict[Any, Any], ndepth: int) -> List[Any]:
    keys = []

    def _extract_keys(json_obj: Dict[Any, Any], curr_depth: int) -> None:
        for key, value in json_obj.items():
            if curr_depth == ndepth:
                keys.append(key)
            elif isinstance(value, dict):
                _extract_keys(value, curr_depth + 1)

    _extract_keys(json_obj, 0)
    return keys


def extract_inner_lists_from_json(json_obj: Dict[Any, Any]) -> List[Any]:
    activities = []
    if isinstance(json_obj, dict):
        for value in json_obj.values():
            activities.extend(extract_inner_lists_from_json(value))
    elif isinstance(json_obj, list):
        activities.extend(json_obj)
    return activities
