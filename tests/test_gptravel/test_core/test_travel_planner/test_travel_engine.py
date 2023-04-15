import pytest

from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


def test_travel_plan_single_city_per_day(
    travel_plan_single_city_per_day: TravelPlanJSON,
):
    days = travel_plan_single_city_per_day.get_key_values_by_name(key_name="day")
    assert days == ["Day 1", "Day 2", "Day 3"]
    cities = travel_plan_single_city_per_day.get_key_values_by_name(key_name="city")
    assert cities == ["Bangkok", "Phuket", "Krabi"]
    activities = travel_plan_single_city_per_day.travel_activities
    assert activities == [
        "Visit Wat Phra Kaew and the Grand Palace",
        "Explore the Wat Pho Temple",
        "Ride a boat in the Chao Phraya River",
        "Shop at Chatuchak weekend market",
        "Spend time at the Patong Beach",
        "Visit Big Buddha Phuket",
        "Explore the Phuket Old Town",
        "Enjoy local street food at night markets",
        "Visit Railay Beach and the Phra Nang Cave",
        "Island hopping tour to Phi Phi Islands",
        "Hike to the Tiger Cave Temple",
        "Relax at Ao Nang Beach",
    ]


def test_travel_plan_multiple_city_per_day(
    travel_plan_multiple_city_per_day_and_wrong_n_days: TravelPlanJSON,
):
    days = travel_plan_multiple_city_per_day_and_wrong_n_days.get_key_values_by_name(
        key_name="day"
    )
    assert days == ["Day 1", "Day 2"]
    cities = travel_plan_multiple_city_per_day_and_wrong_n_days.get_key_values_by_name(
        key_name="city"
    )
    assert cities == ["Bangkok", "Phuket", "Krabi"]
    activities = travel_plan_multiple_city_per_day_and_wrong_n_days.travel_activities
    assert activities == [
        "Visit Wat Phra Kaew and the Grand Palace",
        "Explore the Wat Pho Temple",
        "Ride a boat in the Chao Phraya River",
        "Shop at Chatuchak weekend market",
        "Spend time at the Patong Beach",
        "Visit Big Buddha Phuket",
        "Explore the Phuket Old Town",
        "Enjoy local street food at night markets",
        "Visit Railay Beach and the Phra Nang Cave",
        "Island hopping tour to Phi Phi Islands",
        "Hike to the Tiger Cave Temple",
        "Relax at Ao Nang Beach",
    ]
