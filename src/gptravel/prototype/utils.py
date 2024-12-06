import json
from datetime import date
from typing import Dict, List, Tuple, Union

import openai

from gptravel.core.io.loggerconfig import logger
from gptravel.core.services.engine import classifier
from gptravel.core.services.engine.wikipedia import WikipediaEngine
from gptravel.core.services.score_builder import ScorerOrchestrator
from gptravel.core.services.scorer import TravelPlanScore
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON
from gptravel.core.utils.regex_tool import JsonExtractor
from gptravel.prototype.objects import geo_decoder


def is_valid_openai_key(openai_key: str) -> bool:
    """
    Checks if the provided OpenAI API key is valid by performing a test request.

    Parameters
    ----------
    openai_key : str
        The OpenAI API key to be tested.

    Returns
    -------
    bool
        True if the OpenAI API key is valid and the test request succeeds,
        False otherwise.

    Raises
    ------
    None

    Examples
    --------
    >>> is_valid_openai_key("<OPENAI_API_KEY>")
    True

    >>> is_valid_openai_key("foo")
    False
    """
    openai.api_key = openai_key

    try:
        openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello, World!"},
            ],
            max_tokens=3,
        )
    except openai.BadRequestError:
        return False
    except openai.AuthenticationError:
        return False

    return True


def is_departure_before_return(departure_date: date, return_date: date) -> bool:
    """
    Parameters
    ----------
    departure_date : np.datetime64
        The date of departure.
    return_date : np.datetime64
        The date of return.

    Returns
    -------
    bool_
        True if the departure date is before or equal to the return date, False otherwise.
    """
    return departure_date <= return_date


def get_score_map(
    travel_plan_json: TravelPlanJSON,
) -> TravelPlanScore:
    """
    Calculates the score map for a given travel plan.

    Parameters
    ----------
    travel_plan_json : TravelPlanJSON
        The JSON representation of the travel plan.

    Returns
    -------
    Dict[str, Dict[str, Union[float, int]]]
        A dictionary containing the score map for the travel plan.
    """
    zs_classifier = classifier.ZeroShotTextClassifier(True)
    score_container = TravelPlanScore()
    logger.info("Score Engines: Start")
    scorers_orchestrator = ScorerOrchestrator(
        geocoder=geo_decoder, text_classifier=zs_classifier
    )
    scorers_orchestrator.run(
        travel_plan_json=travel_plan_json, scores_container=score_container
    )
    logger.info("Score Engines: End")
    return score_container


def get_cities_coordinates_of_same_country_destionation(
    cities: Union[List[str], Tuple[str]], destination: str
) -> Dict[str, Tuple[Union[float, None], ...]]:
    logger.info("Get Cities coordinates: Start")
    logger.debug("Get Cities coordinates: cities to analyze = %s", cities)
    logger.debug("Get Cities coordinates: destination = %s", destination)
    destination_country = destination.lower()
    if not is_a_country(destination):
        destination_country = geo_decoder.country_from_location_name(destination)
        if destination_country:
            destination_country = destination_country.lower()
        logger.debug(
            "Get Cities coordinates: destination country = %s", destination_country
        )
    cities_coordinates = {
        city: tuple(coord for coord in geo_decoder.location_coordinates(city).values())
        for city in cities
        if geo_decoder.country_from_location_name(city)
        and geo_decoder.country_from_location_name(city).lower() == destination_country
    }
    logger.info("Get Cities coordinates: End")
    return cities_coordinates


def get_entities_coordinates_of_same_country(
    entities_dict: Dict[str, List[Dict[str, str]]],
    cities: Union[List[str], Tuple[str]],
    destination: str,
) -> Dict[str, Tuple[float, float]]:
    logger.info("Get Entities coordinates: Start")
    destination_country = destination.lower()
    coordinates: Dict[str, Tuple[float, float]] = {}
    if not is_a_country(destination):
        destination_country = geo_decoder.country_from_location_name(destination)
        if destination_country:
            destination_country = destination_country.lower()
    for city in cities:
        country = geo_decoder.country_from_location_name(city)
        if country is not None and country.lower() == destination_country:
            if city in entities_dict.keys():
                for entity_dict in entities_dict[city]:
                    for entity_name in entity_dict.keys():
                        if (entity_name.lower() != city.lower()) and (
                            len(entities_dict[city]) > 1
                        ):
                            name_to_query = entity_name + ", " + city
                            coordinates[entity_name] = tuple(
                                coord
                                for coord in geo_decoder.location_coordinates(
                                    name_to_query
                                ).values()
                            )
                        elif (entity_name.lower() == city.lower()) and (
                            len(entities_dict[city]) == 1
                        ):
                            name_to_query = entity_name
                            coordinates[entity_name] = tuple(
                                coord
                                for coord in geo_decoder.location_coordinates(
                                    name_to_query
                                ).values()
                            )
            else:
                coordinates[city] = tuple(
                    coord for coord in geo_decoder.location_coordinates(city).values()
                )
    logger.info("Get Entities coordinates: End")
    return coordinates


def is_a_country(place: str):
    return geo_decoder.is_a_country(place)


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
        json_dmp = json.dumps(travel_plan.travel_plan)
        travel_plan_string = f"{json_dmp}"
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
