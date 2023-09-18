import json

from gptravel.core.utils.general import (
    extract_inner_list_for_given_key,
    extract_inner_lists_from_json,
    extract_keys_by_depth_from_json,
)


def test_extract_keys_by_depth():
    json_str = '{"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": {"g": {"h": {"i": 4}}}}'
    json_obj = json.loads(json_str)

    assert extract_keys_by_depth_from_json(json_obj, 0) == ["a", "f"]
    assert extract_keys_by_depth_from_json(json_obj, 1) == ["b", "e", "g"]
    assert extract_keys_by_depth_from_json(json_obj, 2) == ["c", "d", "h"]
    assert extract_keys_by_depth_from_json(json_obj, 3) == ["i"]

    json_str = '{"a": {"b": {"c": {"d": {"e": {"f": {"g": 1}}}}}}}'
    json_obj = json.loads(json_str)

    assert extract_keys_by_depth_from_json(json_obj, 0) == ["a"]
    assert extract_keys_by_depth_from_json(json_obj, 1) == ["b"]
    assert extract_keys_by_depth_from_json(json_obj, 2) == ["c"]
    assert extract_keys_by_depth_from_json(json_obj, 3) == ["d"]
    assert extract_keys_by_depth_from_json(json_obj, 4) == ["e"]
    assert extract_keys_by_depth_from_json(json_obj, 5) == ["f"]
    assert extract_keys_by_depth_from_json(json_obj, 6) == ["g"]

    json_str = '{"a": 1, "b": 2, "c": 3}'
    json_obj = json.loads(json_str)

    assert extract_keys_by_depth_from_json(json_obj, 0) == ["a", "b", "c"]
    assert not extract_keys_by_depth_from_json(json_obj, 1)


def test_extract_inner_lists_from_json():
    # Simple example with only one level of nesting
    data = {
        "Day 1": {
            "City 1": ["activity 1", "activity 2"],
            "City 2": ["activity 3", "activity 4"],
        }
    }
    assert extract_inner_lists_from_json(data) == [
        "activity 1",
        "activity 2",
        "activity 3",
        "activity 4",
    ]


def test_extract_inner_lists_more_depth():
    # Simple example with only one level of nesting
    data = {
        "Day 1": {
            "City 1": {"feet": ["activity 1", "activity 2"]},
            "City 2": {"moto": ["activity 3", "activity 4"]},
        },
        "Day 2": {
            "City 1": {"car": ["activity 5", "activity 6"]},
            "City 2": {"boat": ["activity 7", "activity 8"]},
        },
    }
    assert extract_inner_lists_from_json(data) == [
        "activity 1",
        "activity 2",
        "activity 3",
        "activity 4",
        "activity 5",
        "activity 6",
        "activity 7",
        "activity 8",
    ]


def test_extract_inner_list_nested():
    # Example with nested dictionaries and lists
    data = {
        "Day 1": {
            "City 1": ["activity 1", "activity 2"],
            "City 2": ["activity 3", "activity 4"],
        },
        "Day 2": {
            "City 3": ["activity 5", "activity 6"],
            "City 4": [
                {"Subcity 1": ["activity 7", "activity 8"]},
                {"Subcity 2": ["activity 9", "activity 10"]},
            ],
        },
    }
    assert extract_inner_lists_from_json(data) == [
        "activity 1",
        "activity 2",
        "activity 3",
        "activity 4",
        "activity 5",
        "activity 6",
        {"Subcity 1": ["activity 7", "activity 8"]},
        {"Subcity 2": ["activity 9", "activity 10"]},
    ]


def test_extract_inner_list_empty():
    # Example with empty data
    data = {}
    assert not extract_inner_lists_from_json(data)


def test_extract_inner_list_wrong_input():
    # Example with wrong input type
    data = "wrong input type"
    assert not extract_inner_lists_from_json(data)


def test_extract_inner_list_for_given_key():
    # Example with nested dictionaries and lists
    data = {
        "Day 1": {
            "City 1": ["activity 1", "activity 2"],
            "City 2": ["activity 3", "activity 4"],
        },
        "Day 2": {
            "City 1": ["activity 5", "activity 6"],
        },
    }
    assert extract_inner_list_for_given_key(data, "City 1") == [
        "activity 1",
        "activity 2",
        "activity 5",
        "activity 6",
    ]
    assert extract_inner_list_for_given_key(data, "City 2") == [
        "activity 3",
        "activity 4",
    ]
    assert extract_inner_list_for_given_key(data, "City 4") == []
    data = {}
    assert extract_inner_list_for_given_key(data, "City 4") == []
