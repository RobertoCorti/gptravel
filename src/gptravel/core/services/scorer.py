from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from gptravel.core.services.config import ACTIVITIES_LABELS
from gptravel.core.services.geocoder import GeoCoder
from gptravel.core.services.engine.classifier import TextClassifier
from gptravel.core.services.utils import theil_diversity_entropy_index
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class TravelPlanScore:
    def __init__(self) -> None:
        self._score_map: Dict[str, Dict[str, Union[float, int]]] = {}
        self._score_value_key = "score_value"
        self._score_weight_key = "score_weight"
        self._required_keys = set([self._score_value_key, self._score_weight_key])

    def add_score(self, score_type: str, score_dict: Dict[str, Any]) -> None:
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

    @property
    def service_name(self) -> str:
        return self._service_name


class ActivitiesDiversityScorer(ScoreService):
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
        labeled_activities = self._classifier.predict(
            input_text_list=activities_list, label_classes=self._activities_labels
        )
        aggregated_scores = {
            key: sum(item[key] for item in labeled_activities.values())
            for key in self._activities_labels
        }
        sum_scores = sum(aggregated_scores.values())
        aggregated_scores_normalized = {
            key: item / sum_scores for key, item in aggregated_scores.items()
        }
        score = 1.0 - theil_diversity_entropy_index(
            list(aggregated_scores_normalized.values())
        )
        travel_plan_scores.add_score(
            score_type=self._service_name,
            score_dict={
                travel_plan_scores.score_value_key: score,
                travel_plan_scores.score_weight_key: self._score_weight,
                "activities_distribution": aggregated_scores_normalized,
                "labeled_activities": labeled_activities,
            },
        )


class DayGenerationScorer(ScoreService):
    def __init__(
        self, n_days_required: int, score_weight: float = 0.4, day_key: str = "Day"
    ) -> None:
        service_name = "Day Coherence"
        super().__init__(service_name, score_weight)
        self._day_key = day_key
        self._n_days_required = n_days_required

    def score(
        self, travel_plan: TravelPlanJSON, travel_plan_scores: TravelPlanScore
    ) -> None:
        travel_plan_day_list = list(
            set(travel_plan.get_key_values_by_name(self._day_key.lower()))
        )
        travel_plan_days = [
            int(item.split(self._day_key)[-1]) for item in travel_plan_day_list
        ]
        min_day = min(travel_plan_days)
        tot_planned_days = len(travel_plan_days)
        score = (
            1.0 - abs(self._n_days_required - tot_planned_days) / self._n_days_required
        )
        if score < 1:
            self.score_weight = min(self.score_weight * 1.5, 1)
        expected_list = [min_day + item for item in range(self._n_days_required)]
        extra_days_in_travel = set(travel_plan_days) - set(expected_list).intersection(
            travel_plan_days
        )
        missing_days_in_travel = set(expected_list) - set(expected_list).intersection(
            travel_plan_days
        )
        travel_plan_scores.add_score(
            score_type=self._service_name,
            score_dict={
                travel_plan_scores.score_value_key: score,
                travel_plan_scores.score_weight_key: self._score_weight,
                "misaligned_days": {
                    "extra_days": list(extra_days_in_travel),
                    "missing_days": list(missing_days_in_travel),
                },
            },
        )


class CitiesCountryScorer(ScoreService):

    def __init__(
            self, destination: str,  geolocator: GeoCoder, score_weight: float = 1.0 
    ) -> None:
        service_name = "City Countries"
        super().__init__(service_name, score_weight)
        self._geolocator = geolocator
        self._destination = destination

    def score(
        self, travel_plan: TravelPlanJSON, travel_plan_scores: TravelPlanScore
    ) -> None:
        unique_cities = list(travel_plan.travel_cities)
        pass