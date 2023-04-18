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
    geo = GeoCoder()
    score_container = TravelPlanScore()
    scorer = OptimizedItineraryScorer(geo)
    scorer.score(travel_plan=json_travel_plan, travel_plan_scores=score_container)


if __name__ == "__main__":
    main()
