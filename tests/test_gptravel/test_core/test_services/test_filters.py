from copy import deepcopy

import pytest

from gptravel.core.services.filters import DeparturePlaceFilter, TravelPlanJSON


@pytest.fixture
def departure_place_filter() -> DeparturePlaceFilter:
    return DeparturePlaceFilter()


class TestDeparturePlaceFilter:
    def test_on_travel_plan_with_departure(
        self,
        departure_place_filter: DeparturePlaceFilter,
        italian_travel_plan: TravelPlanJSON,
    ):
        before_removal = deepcopy(italian_travel_plan)
        departure_place_filter.filter(italian_travel_plan)
        assert before_removal.travel_plan != italian_travel_plan.travel_plan
        assert (
            italian_travel_plan.departure_place not in italian_travel_plan.travel_cities
        )
        assert italian_travel_plan.get_key_values_by_name("day") == [
            "Day 1",
            "Day 2",
            "Day 3",
        ]
        assert italian_travel_plan.travel_activities == [
            "See San Marco",
            "Take a ride on gondola",
            "Eat an arancina",
            "Eat fiorentina",
        ]

    def test_on_travel_plan_with_nodeparture(
        self,
        departure_place_filter: DeparturePlaceFilter,
        travel_plan_single_city_per_day: TravelPlanJSON,
    ):
        before_removal = deepcopy(travel_plan_single_city_per_day)
        departure_place_filter.filter(travel_plan_single_city_per_day)
        assert (
            travel_plan_single_city_per_day.departure_place
            not in travel_plan_single_city_per_day.travel_cities
        )
        assert before_removal.travel_plan == travel_plan_single_city_per_day.travel_plan
