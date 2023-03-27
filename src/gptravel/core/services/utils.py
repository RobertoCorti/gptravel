import math
from typing import List, Union


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
