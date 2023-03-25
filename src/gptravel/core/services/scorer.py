from abc import ABC, abstractmethod
from typing import Dict, Optional, Union

from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class TravelPlanScore:
    def __init__(self) -> None:
        self._score_map: Dict[str, Dict[str, Union[float, int]]] = {}
        self._score_value_key = "score_value"
        self._score_weight_key = "score_weight"
        self._required_keys = set([self._score_value_key, self._score_weight_key])

    def add_score(
        self, score_type: str, score_dict: Dict[str, Union[float, int]]
    ) -> None:
        assert (score_dict.keys()) == self._required_keys
        self._score_map.update({score_type: score_dict})

    @property
    def score_value_key(self) -> str:
        return self._score_value_key

    @property
    def score_weight_key(self) -> str:
        return self._score_value_key

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


class ScoreService(ABC):
    def __init__(self, service_name: str, score_weight: float) -> None:
        self._service_name = service_name
        self.score_weight = score_weight

    @abstractmethod
    def score(
        self, travel_plan: TravelPlanJSON, travel_plan_scores: TravelPlanScore
    ) -> None:
        pass

    @property
    def score_weight(self) -> float:
        return self._score_weight

    @score_weight.setter
    def score_weight(self, score_weight: float) -> None:
        assert (score_weight >= 0.0) & (score_weight <= 1.0)
        self._score_weight = score_weight


class ScoreActivitiesVariety(ScoreService):
    def __init__(self, score_weight: float = 0.7) -> None:
        service_name = "Activities Variety"
        super().__init__(service_name, score_weight)

    def score(
        self, travel_plan: TravelPlanJSON, travel_plan_scores: TravelPlanScore
    ) -> None:
        activities_list = travel_plan.travel_activities
        score = len(set(activities_list)) / len(activities_list)
        travel_plan_scores.add_score(
            score_type=self._service_name,
            score_dict={
                travel_plan_scores.score_value_key: score,
                travel_plan_scores.score_weight_key: self._score_weight,
            },
        )
        labels = ["mountain", "city", "sea", "museum", "monument", "food", "relax", "sport", "history", "culture"]
