from gptravel.core.services.geocoder import GeoCoder
from gptravel.core.services.scorer import (
    CitiesCountryScorer,
    DayGenerationScorer,
    OptimizedItineraryScorer,
    TravelPlanScore,
)
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


def main():
    json_travel_plan = TravelPlanJSON(
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
    geo = GeoCoder()
    score_container = TravelPlanScore()
    scorer = OptimizedItineraryScorer(geo)
    scorer.score(travel_plan=json_travel_plan, travel_plan_scores=score_container)


if __name__ == "__main__":
    main()
