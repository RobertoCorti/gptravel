from typing import Any, Dict, List

import pytest

from gptravel.core.travel_planner.prompt import PromptFactory
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


@pytest.fixture
def travel_plan_single_city_per_day() -> TravelPlanJSON:
    json_travel_plan = TravelPlanJSON(
        destination_place="Thailand",
        departure_place="Milan",
        n_days=3,
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
def travel_plan_multiple_city_per_day_and_wrong_n_days() -> TravelPlanJSON:
    json_travel_plan = TravelPlanJSON(
        departure_place="Milan",
        destination_place="Thailand",
        n_days=3,
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
def travel_plan_multiple_city_per_day_and_wrong_city_per_country() -> TravelPlanJSON:
    json_travel_plan = TravelPlanJSON(
        departure_place="Milan",
        destination_place="Thailand",
        n_days=2,
        json_keys_depth_map={"day": 0, "city": 1},
        travel_plan_json={
            "Day 1": {
                "Bangkok": [
                    "Visit Wat Phra Kaew and the Grand Palace",
                    "Explore the Wat Pho Temple",
                    "Ride a boat in the Chao Phraya River",
                    "Shop at Chatuchak weekend market",
                ],
                "Milan": [
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
def travel_plan_fake_city() -> TravelPlanJSON:
    json_travel_plan = TravelPlanJSON(
        departure_place="Milan",
        destination_place="Thailand",
        n_days=2,
        json_keys_depth_map={"day": 0, "city": 1},
        travel_plan_json={
            "Day 1": {
                "Bangkok": [
                    "Visit Wat Phra Kaew and the Grand Palace",
                    "Explore the Wat Pho Temple",
                    "Ride a boat in the Chao Phraya River",
                    "Shop at Chatuchak weekend market",
                ],
                "ChromeCastFrancesco": [
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
def italian_travel_plan() -> TravelPlanJSON:
    return TravelPlanJSON(
        destination_place="Italy",
        departure_place="Paris",
        n_days=4,
        travel_plan_json={
            "Day 1": {
                "Paris": [
                    "Take flight to Venice",
                ]
            },
            "Day 2": {
                "Venice": [
                    "See San Marco",
                ]
            },
            "Day 3": {
                "Venice": [
                    "Take a ride on gondola",
                ],
                "Palermo": ["Eat an arancina"],
            },
            "Day 4": {"Florence": ["Eat fiorentina"], "Paris": ["Return back home"]},
        },
        json_keys_depth_map={"city": 1, "day": 0},
    )


@pytest.fixture
def travel_properties() -> Dict[str, Any]:
    return {
        "departure_place": "Milan",
        "destination_place": "Thailand",
        "n_travel_days": 10,
    }


@pytest.fixture
def prompt_factory() -> PromptFactory:
    return PromptFactory()


@pytest.fixture()
def labels_activities() -> List[str]:
    return [
        "mountain",
        "sea",
        "museum",
        "monument",
        "food",
        "relax",
        "sport",
        "culture",
        "shopping",
        "transport",
    ]
