from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class TestTravelPlanJSON:
    def test_travel_plan_properties(
        self, travel_plan_single_city_per_day: TravelPlanJSON
    ):
        assert travel_plan_single_city_per_day.n_days == 3
        assert travel_plan_single_city_per_day.departure_place == "Milan"
        assert travel_plan_single_city_per_day.destination_place == "Thailand"
        assert travel_plan_single_city_per_day.keys_map == {"day": 0, "city": 1}
        assert travel_plan_single_city_per_day.travel_plan == {
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
        }
        assert travel_plan_single_city_per_day.get_travel_activities_from_city(
            "Phuket"
        ) == [
            "Spend time at the Patong Beach",
            "Visit Big Buddha Phuket",
            "Explore the Phuket Old Town",
            "Enjoy local street food at night markets",
        ]
        assert travel_plan_single_city_per_day.get_travel_activities_from_city(
            "Bangkok"
        ) == [
            "Visit Wat Phra Kaew and the Grand Palace",
            "Explore the Wat Pho Temple",
            "Ride a boat in the Chao Phraya River",
            "Shop at Chatuchak weekend market",
        ]

    def test_travel_plan_single_city_per_day(
        self,
        travel_plan_single_city_per_day: TravelPlanJSON,
    ):
        days = travel_plan_single_city_per_day.get_key_values_by_name(key_name="day")
        assert days == ["Day 1", "Day 2", "Day 3"]
        cities = travel_plan_single_city_per_day.get_key_values_by_name(key_name="city")
        assert cities == ["Bangkok", "Phuket", "Krabi"]
        key_values = travel_plan_single_city_per_day.get_key_values_by_name(
            key_name="rr"
        )
        assert key_values == []
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
        self,
        travel_plan_multiple_city_per_day_and_wrong_n_days: TravelPlanJSON,
    ):
        days = (
            travel_plan_multiple_city_per_day_and_wrong_n_days.get_key_values_by_name(
                key_name="day"
            )
        )
        assert days == ["Day 1", "Day 2"]
        cities = (
            travel_plan_multiple_city_per_day_and_wrong_n_days.get_key_values_by_name(
                key_name="city"
            )
        )
        assert cities == ["Bangkok", "Phuket", "Krabi"]
        activities = (
            travel_plan_multiple_city_per_day_and_wrong_n_days.travel_activities
        )
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
