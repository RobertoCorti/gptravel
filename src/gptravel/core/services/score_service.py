from typing import Dict, Optional, Union


class TravelPlanScore:
    def __init__(self) -> None:
        self._score_map: Dict[str, Dict[str, Union[float, int]]] = {}
        self._required_keys = set(["score_value", "score_weight"])

    def add_score(
        self, score_type: str, score_dict: Dict[str, Union[float, int]]
    ) -> None:
        assert (score_dict.keys()) == self._required_keys
        self._score_map.update({score_type: score_dict})

    @property
    def score_map(self) -> Dict[str, Dict[str, Union[float, int]]]:
        return self._score_map

    @property
    def weighted_score(self) -> Optional[float]:
        if self._score_map:
            total_weight = sum(
                score["score_weight"] for score in self._score_map.values()
            )
            weighted_sum = sum(
                score["score_value"] * score["score_weight"]
                for score in self._score_map.values()
            )
            return weighted_sum / total_weight
        return None
