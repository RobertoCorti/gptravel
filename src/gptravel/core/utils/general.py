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
    inner_list = []
    if isinstance(json_obj, dict):
        for value in json_obj.values():
            inner_list.extend(extract_inner_lists_from_json(value))
    elif isinstance(json_obj, list):
        inner_list.extend(json_obj)
    return inner_list


def extract_inner_list_for_given_key(json_obj: Dict[Any, Any], key: Any) -> List[Any]:
    """
    Extracts all lists associated with the given key from a dictionary of undefined depth.

    Args:
        dictionary (dict): The input dictionary.
        key: The key to search for.

    Returns:
        list: The extracted lists if the key is found, otherwise an empty list.
    """
    lists = (
        [json_obj[key]] if key in json_obj and isinstance(json_obj[key], list) else []
    )

    nested_lists = [
        extract_inner_list_for_given_key(value, key)
        for value in json_obj.values()
        if isinstance(value, (dict))
    ]

    return [item for sublist in lists + nested_lists for item in sublist]
