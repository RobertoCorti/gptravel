from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, Optional, Union

from gptravel.core.services.config import ACTIVITIES_LABELS
from gptravel.core.services.engine.classifier import TextClassifier
from gptravel.core.services.utils import entropy_score
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
        assert set(score_dict.keys()).intersection(self._required_keys) == set(
            self._required_keys
        )
        self._score_map.update({score_type: score_dict})

    @property
    def score_value_key(self) -> str:
        return self._score_value_key

    @property
    def score_weight_key(self) -> str:
        return self._score_weight_key

    @property
    def score_map(self) -> Dict[str, Dict[str, Union[float, int]]]:
        return self._score_map

    @property
    def weighted_score(self) -> Optional[float]:
        if self._score_map:
            total_weight = sum(
                score[self._score_weight_key] for score in self._score_map.values()
            )
            weighted_sum = sum(
                score[self._score_value_key] * score[self._score_weight_key]
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


class ActivitiesVarietyPlainScorer(ScoreService):
    def __init__(self, score_weight: float = 0.7) -> None:
        service_name = "Plain Activities Variety"
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


class ActivitiesVarietyClassifierScorer(ScoreService):
    def __init__(
        self, text_classifier: TextClassifier, score_weight: float = 0.8
    ) -> None:
        service_name = "Activities Variety"
        super().__init__(service_name, score_weight)
        self._classifier = text_classifier
        self._activities_labels = ACTIVITIES_LABELS

    def score(
        self, travel_plan: TravelPlanJSON, travel_plan_scores: TravelPlanScore
    ) -> None:
        activities_list = travel_plan.travel_activities
        class_scores = self._classifier.predict(
            input_text_list=activities_list, label_classes=self._activities_labels
        )
        aggregated_scores = {
            key: sum(item[key] for item in class_scores)
            for key in self._activities_labels
        }
        sum_scores = sum(aggregated_scores.values())
        aggregated_scores_normalized = {
            key: item / sum_scores for key, item in aggregated_scores.items()
        }
        score = entropy_score(list(aggregated_scores_normalized.values()))
        travel_plan_scores.add_score(
            score_type=self._service_name,
            score_dict={
                travel_plan_scores.score_value_key: score,
                travel_plan_scores.score_weight_key: self._score_weight,
                "activities_distribution": aggregated_scores_normalized,
            },
        )


if __name__ == "__main__":
    from gptravel.core.services.engine.classifier import ZeroShotTextClassifier

    a = ZeroShotTextClassifier(True)
    scores = TravelPlanScore()
    scorer = ActivitiesVarietyClassifierScorer(text_classifier=a)
    out = scorer.score(
        TravelPlanJSON(
            travel_plan_json={
                "Day 1": {
                    "Bangkok": [
                        "Visit Wat Phra Kaew and the Grand Palace",
                        "Explore the Wat Pho Temple",
                        "Ride a boat in the Chao Phraya River",
                        "Shop at Chatuchak weekend market",
                    ]
                },
                "Day 2": {
                    "Phuket": [
                        "Spend time at the Patong Beach",
                        "Visit Big Buddha Phuket",
                        "Explore the Phuket Old Town",
                        "Enjoy local street food at night markets",
                    ]
                },
                "Day 3": {
                    "Krabi": [
                        "Visit Railay Beach and the Phra Nang Cave",
                        "Island hopping tour to Phi Phi Islands",
                        "Hike to the Tiger Cave Temple",
                        "Relax at Ao Nang Beach",
                    ]
                },
            },
            json_keys_depth_map={"city": 1, "day": 0},
        ),
        scores,
    )
