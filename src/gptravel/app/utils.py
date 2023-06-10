import datetime
from typing import Any, Dict, Tuple

import pycountry
from geopy.geocoders.base import Geocoder

from gptravel.core.services import geocoder, score_builder, scorer
from gptravel.core.services.engine import classifier
from gptravel.core.travel_planner import openai_engine
from gptravel.core.travel_planner.prompt import PromptFactory
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON

MAX_TOKENS = 1024


def get_score_description(score: float) -> str:
    """
    Returns a description based on the given score.

    Parameters:
    - score (float): The score to describe. Should be in the range of 0 to 10 (inclusive).

    Returns:
    - str: A description of the score.

    """
    if 0 <= score < 2:
        return "The score is very low."
    elif 2 <= score < 4:
        return "The score is low."
    elif 4 <= score < 6:
        return "The score is medium."
    elif 6 <= score < 8:
        return "The score is high."
    elif 8 <= score <= 10:
        return "The score is very high."


def get_travel_cities_coordinates(travel_plan_dict: dict, geocoder: Geocoder) -> dict:
    return {
        day: {
            city: [geocoder.geocode(city).latitude, geocoder.geocode(city).longitude]
            for city in day_activity.keys()
        }
        for day, day_activity in travel_plan_dict.items()
    }


def calculate_number_of_days(return_date, departure_date):
    """
    Calculates the number of travel days based on the departure and return dates.

    Args:
        return_date (str): Return date in the format 'YYYY-MM-DD'.
        departure_date (str): Departure date in the format 'YYYY-MM-DD'.

    Returns:
        int: Number of travel days.
    """
    n_days = (
        datetime.datetime.strptime(return_date, "%Y-%m-%d")
        - datetime.datetime.strptime(departure_date, "%Y-%m-%d")
    ).days
    return n_days


def get_country_names(departure, destination):
    """
    Retrieves the country names based on the departure and destination codes.

    Args:
        departure (str): Departure code or name.
        destination (str): Destination code or name.

    Returns:
        tuple: Tuple containing departure country name and destination country name.
    """
    try:
        departure_country_name = pycountry.countries.get(alpha_2=departure).name
        destination_country_name = pycountry.countries.get(alpha_2=destination).name
    except AttributeError:
        destination_country_name = destination
        departure_country_name = departure
    return departure_country_name, destination_country_name


def build_travel_parameters(
    departure: str, destination: str, n_days: int, travel_option: str
) -> Dict[str, Any]:
    """
    Builds the travel parameters dictionary.

    Args:
        departure (str): Departure country name.
        destination (str): Destination country name.
        n_days (int): Number of travel days.
        travel_option (str): Travel option.

    Returns:
        dict: Travel parameters dictionary.
    """
    travel_parameters = {
        "departure_place": departure,
        "destination_place": destination,
        "n_travel_days": n_days,
        "travel_theme": travel_option,
    }
    return travel_parameters


def build_prompt(travel_parameters: Dict[str, Any]) -> str:
    """
    Builds the prompt for the travel plan based on the travel parameters.

    Args:
        travel_parameters (dict): Travel parameters.

    Returns:
        str: Prompt for the travel plan.
    """
    prompt_factory = PromptFactory()
    prompt = prompt_factory.build_prompt(**travel_parameters)
    return prompt


def get_travel_plan_json(prompt: str) -> TravelPlanJSON:
    """
    Retrieves the travel plan JSON based on the provided prompt.

    Args:
        prompt (str): Prompt for the travel plan.

    Returns:
        TravelPlanJSON: Travel plan JSON.
    """
    engine = openai_engine.ChatGPTravelEngine(max_tokens=MAX_TOKENS)
    return engine.get_travel_plan_json(prompt)


def calculate_travel_score(travel_plan_dict: Dict[str, Any]) -> float:
    """
    Calculates the travel score based on the travel plan.

    Args:
        travel_plan_dict (dict): Travel plan dictionary.

    Returns:
        float: Travel score.
    """
    zs_classifier = classifier.ZeroShotTextClassifier(True)
    geo_decoder = geocoder.GeoCoder()
    score_container = scorer.TravelPlanScore()
    scorers_orchestrator = score_builder.ScorerOrchestrator(
        geocoder=geo_decoder, text_classifier=zs_classifier
    )
    scorers_orchestrator.run(
        travel_plan_json=travel_plan_dict, scores_container=score_container
    )
    score = round(score_container.weighted_score * 10, 1)
    return score
