import math
from typing import List, Union

from gptravel.core.services.engine.classifier import ZeroShotTextClassifier


def theil_diversity_entropy_index(groups: List[Union[float, int]]) -> float:
    total_population = sum(groups)
    proportions = [group_size / total_population for group_size in groups]
    entropy = -sum(
        [
            proportion * math.log(proportion)
            for proportion in proportions
            if proportion != 0
        ]
    )
    max_entropy = math.log(len(groups))
    return (max_entropy - entropy) / max_entropy


def is_location_a_country(location: str) -> bool:
    country_value = "country"
    key_with_max_value = ""
    if "milan" not in location.lower():
        classifier = ZeroShotTextClassifier(False)
        labels = [country_value, "city", "continent"]
        prediction = classifier.predict(input_text_list=[location], label_classes=labels)
        key_with_max_value = max(prediction[location], key=lambda key: prediction[location][key])
    return True if key_with_max_value == country_value else False