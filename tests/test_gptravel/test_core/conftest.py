from typing import Any, Dict

import pytest

from gptravel.core.services.geocoder import GeoCoder
from gptravel.core.services.scorer import DayGenerationScorer, TravelPlanScore
from gptravel.core.travel_planner.prompt import PromptFactory
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON
from gptravel.core.utils.regex import JsonExtractor


@pytest.fixture
def travel_plan_single_city_per_day() -> TravelPlanJSON:
    json_travel_plan = TravelPlanJSON(
        json_keys_depth_map={"day": 0, "city": 1},
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
    )
    return json_travel_plan


@pytest.fixture
def travel_plan_multiple_city_per_day() -> TravelPlanJSON:
    json_travel_plan = TravelPlanJSON(
        json_keys_depth_map={"day": 0, "city": 1},
        travel_plan_json={
            "Day 1": {
                "Bangkok": [
                    "Visit Wat Phra Kaew and the Grand Palace",
                    "Explore the Wat Pho Temple",
                    "Ride a boat in the Chao Phraya River",
                    "Shop at Chatuchak weekend market",
                ],
                "Phuket": [
                    "Spend time at the Patong Beach",
                    "Visit Big Buddha Phuket",
                    "Explore the Phuket Old Town",
                    "Enjoy local street food at night markets",
                ],
            },
            "Day 2": {
                "Krabi": [
                    "Visit Railay Beach and the Phra Nang Cave",
                    "Island hopping tour to Phi Phi Islands",
                    "Hike to the Tiger Cave Temple",
                    "Relax at Ao Nang Beach",
                ]
            },
        },
    )
    return json_travel_plan


@pytest.fixture
def travel_properties() -> Dict[str, Any]:
    return {
        "travel_departure": "Milan",
        "travel_destination": "Thailand",
        "n_travel_days": 10,
    }


@pytest.fixture
def prompt_factory() -> PromptFactory:
    return PromptFactory()


@pytest.fixture
def geo_coder():
    return GeoCoder()


@pytest.fixture
def score_container() -> TravelPlanScore:
    return TravelPlanScore()


@pytest.fixture
def extractor() -> JsonExtractor:
    return JsonExtractor()


@pytest.fixture
def day_generation_scorer() -> DayGenerationScorer:
    return DayGenerationScorer(n_days_required=3)
