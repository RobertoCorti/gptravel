import json
import os
import time
from typing import Optional

import openai
from dotenv import load_dotenv

from gptravel.core.services.checker import DaysChecker, ExistingDestinationsChecker
from gptravel.core.services.engine.classifier import ZeroShotTextClassifier
from gptravel.core.services.filters import DeparturePlaceFilter
from gptravel.core.services.geocoder import GeoCoder
from gptravel.core.services.score_builder import ScorerOrchestrator
from gptravel.core.services.scorer import TravelPlanScore
from gptravel.core.travel_planner.openai_engine import ChatGPTravelEngine
from gptravel.core.travel_planner.prompt import PromptFactory

# from gptravel.core.travel_planner.travel_engine import TravelPlanJSON

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def main(
    destination_place: str,
    departure_place: str,
    n_days: int,
    travel_theme: Optional[str] = None,
):
    start_time = time.time()
    travel_parameters = {
        "departure_place": departure_place,
        "destination_place": destination_place,
        "n_travel_days": n_days,
        "travel_theme": travel_theme,
    }

    prompt_factory = PromptFactory()

    prompt = prompt_factory.build_prompt(**travel_parameters)

    engine = ChatGPTravelEngine(max_tokens=350)
    travel_plan_in_json_format = engine.get_travel_plan_json(prompt)
    travel_plan_in_json_format = engine.get_travel_plan_json(prompt)
    print(
        "** Execution time for travel generation", time.time() - start_time, "seconds"
    )
    with open(
        "trave-l_plan_{}_{}.json".format(destination_place, n_days), "w"
    ) as jfile:
        json.dump(travel_plan_in_json_format.travel_plan, jfile)

    """travel_plan_in_json_format = TravelPlanJSON(
        destination_place="Malaysia",
        departure_place="Rome",
        n_days=4,
        travel_plan_json={
            "Day 1": {
                "Kuala Lumpur": [
                    "Visit Petronas Towers",
                    "Explore Batu Caves",
                    "Shop at Central Market",
                    "Try local street food at Jalan Alor",
                ]
            },
            "Day 2": {
                "Kuala Lumpur": [
                    "Visit Islamic Arts Museum",
                    "Explore Merdeka Square",
                    "Enjoy panoramic views from KL Tower",
                ]
            },
            "Day 3": {
                "Penang": [
                    "Discover George Town's street art",
                    "Visit Kek Lok Si Temple",
                    "Try local food at Gurney Drive Hawker Centre",
                ]
            },
        },
        json_keys_depth_map={"city": 1, "day": 0},
    )"""
    filter_service = DeparturePlaceFilter()
    filter_service.filter(travel_plan=travel_plan_in_json_format)
    checker = DaysChecker()
    is_ok = checker.check(travel_plan=travel_plan_in_json_format)
    if not is_ok:
        travel_parameters["complention_travel_plan"] = True
        travel_parameters["n_days_to_add"] = (
            travel_plan_in_json_format.n_days - checker.travel_days
        )
        travel_parameters["travel_plan"] = travel_plan_in_json_format.travel_plan
        prompt_completion = prompt_factory.build_prompt(**travel_parameters)
        travel_plan_in_json_format = engine.get_travel_plan_json(prompt_completion)
    middle_time = time.time()
    zs_classifier = ZeroShotTextClassifier(True)
    geo_decoder = GeoCoder()
    score_container = TravelPlanScore()
    city_checker = ExistingDestinationsChecker(geo_decoder)
    good = city_checker.check(travel_plan_in_json_format)
    scorers_orchestrator = ScorerOrchestrator(
        geocoder=geo_decoder, text_classifier=zs_classifier
    )
    scorers_orchestrator.run(
        travel_plan_json=travel_plan_in_json_format, scores_container=score_container
    )
    print(
        "** Execution time for scores computation", time.time() - middle_time, "seconds"
    )
    print("** Total execution time", time.time() - start_time, "seconds")
    print("** Travel plan overall scores", score_container.weighted_score)
    with open(
        "trave-l_plan_{}_{}_scores.json".format(destination_place, n_days), "w"
    ) as jfile:
        json.dump(score_container.score_map, jfile)


if __name__ == "__main__":
    main(
        destination_place="Malaysia",
        departure_place="Milan",
        n_days=4,
        travel_theme=None,
    )
