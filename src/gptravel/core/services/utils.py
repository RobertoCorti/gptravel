import math
from typing import Any, List, Union

from gptravel.core.services.engine.classifier import ZeroShotTextClassifier


def theil_diversity_entropy_index(groups: List[Union[float, int]]) -> float:
    total_population = sum(groups)
    proportions = [group_size / total_population for group_size in groups]
    entropy = -1.0 * sum(
        proportion * math.log(proportion)
        for proportion in proportions
        if proportion != 0
    )
    max_entropy = math.log(len(groups))
    return (max_entropy - entropy) / max_entropy


def weighted_average(
    values: List[Union[int, float]], weights: List[Union[int, float]]
) -> float:
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length.")
    return sum(values[i] * weights[i] for i in range(len(values))) / sum(weights)


def is_location_a_country(location: str) -> bool:
    country_value = "country"
    key_with_max_value = ""
    if "milan" not in location.lower():
        classifier = ZeroShotTextClassifier(False)
        labels = [country_value, "city", "continent"]
        prediction = classifier.predict(
            input_text_list=[location], label_classes=labels
        )
        # ensure the prediction is not None before proceeding
        if prediction and location in prediction:
            key_with_max_value = max(
                prediction[location], key=lambda key: prediction[location][key]
            )
    return key_with_max_value == country_value


def remove_consecutive_duplicates(input_list: List[Any]) -> List[Any]:
    return [
        elem for i, elem in enumerate(input_list) if i == 0 or input_list[i - 1] != elem
    ]
