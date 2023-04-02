from gptravel.core.services.engine.classifier import ZeroShotTextClassifier
from gptravel.core.services.scorer import ActivitiesDiversityScorer, TravelPlanScore
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON

if __name__ == "__main__":
    a = ZeroShotTextClassifier(True)
    scores = TravelPlanScore()
    scorer = ActivitiesDiversityScorer(text_classifier=a)
    scorer.score(
        TravelPlanJSON(
            travel_plan_json={
                "Day 1": {
                    "Kuta": [
                        "Surfing lessons at Kuta Beach",
                        "Visit Waterbom Bali Water Park",
                        "Shopping at Kuta Art Market",
                    ]
                },
                "Day 2": {
                    "Ubud": [
                        "Visit Tegalalang Rice Terrace",
                        "Explore the Sacred Monkey Forest Sanctuary",
                        "Visit Ubud Palace and Ubud Market",
                    ]
                },
                "Day 3": {
                    "Seminyak": [
                        "Explore Seminyak's Sunset Beach",
                        "Luxury spa treatments at The Spa at Peppers Seminyak",
                        "Dinner at Sarong Restaurant",
                    ]
                },
            },
            json_keys_depth_map={"city": 1, "day": 0},
        ),
        scores,
    )
    print(scores.score_map)
