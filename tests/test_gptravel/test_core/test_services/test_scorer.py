import pytest

from gptravel.core.services.scorer import (
    CitiesCountryScorer,
    DayGenerationScorer,
    TravelPlanScore,
)
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class TestTravelPlanScore:
    def test_add_score(self, score_container: TravelPlanScore):
        score_container.add_score(
            "type score", {"score_value": 100, "score_weight": 0.11}
        )
        score_container.add_score(
            "score livel", {"score_value": 80, "score_weight": 0.23}
        )
        score_container.add_score(
            "score basso", {"score_value": 60, "score_weight": 0.15}
        )
        score_container.add_score(
            "score extra", {"score_value": 90, "score_weight": 0.10}
        )
        assert score_container.score_map["score extra"] == {
            "score_value": 90,
            "score_weight": 0.10,
        }

    def test_weighted_score(self, score_container: TravelPlanScore):
        score_container.add_score(
            "type score", {"score_value": 100, "score_weight": 0.11}
        )
        score_container.add_score(
            "score livel", {"score_value": 80, "score_weight": 0.23}
        )
        score_container.add_score(
            "score basso", {"score_value": 60, "score_weight": 0.15}
        )
        assert score_container.weighted_score == pytest.approx(78.367, 0.001)

    def test_weighted_score_empty(self, score_container: TravelPlanScore):
        assert score_container.weighted_score == None

    def test_add_score_missing_key(self):
        score = TravelPlanScore()
        with pytest.raises(AssertionError):
            score.add_score("score extra", {"score_value": 90})


class TestDayGenerationScorer:
    def test_day_generation_scorer_with_correct_days_travel_plan(
        self,
        score_container: TravelPlanScore,
        travel_plan_single_city_per_day: TravelPlanJSON,
        day_generation_scorer: DayGenerationScorer,
    ) -> None:
        day_generation_scorer.score(
            travel_plan=travel_plan_single_city_per_day,
            travel_plan_scores=score_container,
        )
        assert list(score_container.score_map.keys()) == [
            day_generation_scorer.service_name
        ]
        score_dict = score_container.score_map[day_generation_scorer.service_name]
        assert score_dict["score_value"] == 1.0
        assert score_dict["score_weight"] == 0.4
        assert score_dict["misaligned_days"]["extra_days"] == []
        assert score_dict["misaligned_days"]["missing_days"] == []

    def test_day_generation_scorer_with_no_correct_days_travel_plan(
        self,
        score_container: TravelPlanScore,
        travel_plan_multiple_city_per_day_and_wrong_n_days: TravelPlanJSON,
        day_generation_scorer: DayGenerationScorer,
    ) -> None:
        day_generation_scorer.score(
            travel_plan=travel_plan_multiple_city_per_day_and_wrong_n_days,
            travel_plan_scores=score_container,
        )
        assert list(score_container.score_map.keys()) == [
            day_generation_scorer.service_name
        ]
        score_dict = score_container.score_map[day_generation_scorer.service_name]
        assert score_dict["score_value"] == pytest.approx(0.67, 0.01)
        assert score_dict["score_weight"] == pytest.approx(0.6, 0.01)
        assert score_dict["misaligned_days"]["extra_days"] == []
        assert score_dict["misaligned_days"]["missing_days"] == [3]


class TestCitiesCountryScorer:
    def test_with_correct_travel_plan(
        self,
        cities_country_scorer: CitiesCountryScorer,
        travel_plan_multiple_city_per_day_and_wrong_n_days: TravelPlanJSON,
        score_container: TravelPlanScore,
    ) -> None:
        cities_country_scorer.score(
            travel_plan_multiple_city_per_day_and_wrong_n_days, score_container
        )
        score_dict = score_container.score_map[cities_country_scorer.service_name]
        assert score_dict["score_value"] == pytest.approx(1.0, 0.01)
        assert score_dict["latitude_check"]["score"] == pytest.approx(1.0, 0.01)
        assert score_dict["country_check"]["score"] == pytest.approx(1.0, 0.01)

    def test_with_wrong_city_travel_plan(
        self,
        cities_country_scorer: CitiesCountryScorer,
        travel_plan_multiple_city_per_day_and_wrong_city_per_country: TravelPlanJSON,
        score_container: TravelPlanScore,
    ) -> None:
        cities_country_scorer.score(
            travel_plan_multiple_city_per_day_and_wrong_city_per_country,
            score_container,
        )
        score_dict = score_container.score_map[cities_country_scorer.service_name]
        assert score_dict["score_value"] == pytest.approx(0.8, 0.01)
        assert score_dict["latitude_check"]["score"] == pytest.approx(1.0, 0.01)
        assert score_dict["country_check"]["score"] == pytest.approx(0.666, 0.01)
