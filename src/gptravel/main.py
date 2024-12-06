import json
import os
import time
from typing import Dict, List, Optional

import openai
from dotenv import load_dotenv

from gptravel.core.io.loggerconfig import logger
from gptravel.core.services.checker import DaysChecker, ExistingDestinationsChecker
from gptravel.core.services.engine.classifier import ZeroShotTextClassifier
from gptravel.core.services.engine.entity_recognizer import EntityRecognizer
from gptravel.core.services.engine.wikipedia import WikipediaEngine
from gptravel.core.services.filters import DeparturePlaceFilter
from gptravel.core.services.geocoder import Geocoder
from gptravel.core.services.score_builder import ScorerOrchestrator
from gptravel.core.services.scorer import ActivityPlacesScorer, TravelPlanScore
from gptravel.core.travel_planner.openai_engine import ChatGPTravelEngine
from gptravel.core.travel_planner.prompt import PromptFactory
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON
from gptravel.core.utils.regex_tool import JsonExtractor

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_wiki_urls_from_city_entities(
    city_with_entity_map: Dict[str, List[Dict[str, str]]]
) -> Dict[str, List[Dict[str, str]]]:
    wiki = WikipediaEngine()
    output_map: Dict[str, List[Dict[str, str]]] = {}
    for city in city_with_entity_map.keys():
        list_of_entities = city_with_entity_map[city]
        entities_list_with_url: List[Dict[str, str]] = []
        for entity in list_of_entities:
            entity_name = list(entity.keys())[0]
            trials = [
                entity_name + ", " + city,
                entity_name + " of " + city,
                entity_name,
            ]
            found_url = False
            for trial in trials:
                page_url = wiki.url(trial)
                if page_url:
                    logger.debug("Wikipedia-page url for entity %s found", entity_name)
                    entities_list_with_url.append({entity_name: page_url})
                    found_url = True
                    break
            if not found_url:
                logger.warning(
                    "Wikipedia-page url for entity %s not found", entity_name
                )
        if len(entities_list_with_url) > 0:
            output_map[city] = entities_list_with_url
    return output_map


def modify_travel_plan_with_entity_urls_using_mkd(
    entities_with_urls: Dict[str, List[Dict[str, str]]], travel_plan: TravelPlanJSON
) -> TravelPlanJSON:
    if len(entities_with_urls) > 0:
        tp_dumped = json.dumps(travel_plan.travel_plan)
        travel_plan_string = f"{tp_dumped}"
        for city in entities_with_urls.keys():
            entities_in_city = entities_with_urls[city]
            for entity_dict in entities_in_city:
                for entity_name, value in entity_dict.items():
                    if entity_name.lower() != city.lower():
                        entity_with_url_in_mkd = f"[{entity_name}]({value})"
                        travel_plan_string = travel_plan_string.replace(
                            entity_name, entity_with_url_in_mkd
                        )
        regex = JsonExtractor()
        return TravelPlanJSON(
            departure_place=travel_plan.departure_place,
            destination_place=travel_plan.destination_place,
            n_days=travel_plan.n_days,
            json_keys_depth_map=travel_plan.keys_map,
            travel_plan_json=json.loads(regex(travel_plan_string)[0]),
        )
    return travel_plan


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

    prompt_factory.build_prompt(**travel_parameters)

    engine = ChatGPTravelEngine(max_tokens=350)
    # travel_plan_in_json_format = engine.get_travel_plan_json(prompt)
    print(
        "** Execution time for travel generation", time.time() - start_time, "seconds"
    )
    # with open(
    #    "trave-l_plan_{}_{}.json".format(destination_place, n_days), "w"
    # ) as jfile:
    #    json.dump(travel_plan_in_json_format.travel_plan, jfile)

    travel_plan_in_json_format = TravelPlanJSON(
        destination_place="Malaysia",
        departure_place="Rome",
        n_days=3,
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
    )
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
    geo_decoder = Geocoder()
    score_container = TravelPlanScore()
    city_checker = ExistingDestinationsChecker(geo_decoder)
    city_checker.check(travel_plan_in_json_format)
    scorer_activities = ActivityPlacesScorer(
        geolocator=geo_decoder, entity_recognizer=EntityRecognizer()
    )
    scorer_activities.score(
        travel_plan=travel_plan_in_json_format, travel_plan_scores=score_container
    )
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
    with open(f"trave-l_plan_{destination_place}_{n_days}_scores.json", "w") as jfile:
        json.dump(score_container.score_map, jfile)


if __name__ == "__main__":
    main(
        destination_place="Malaysia",
        departure_place="Milan",
        n_days=3,
        travel_theme=None,
    )
