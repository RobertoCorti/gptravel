import datetime
from typing import Dict, Any, Union

import pycountry
import allcities
import openai

from gptravel.core.services.engine import classifier
from gptravel.core.services.scorer import TravelPlanScore, ActivitiesDiversityScorer
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON

COUNTRIES = [country.name.lower() for country in pycountry.countries]
CITIES = [city.name.lower() for city in allcities.cities]


def is_valid_location(location: str) -> bool:
    """
    Check if a location is valid.

    Parameters
    ----------
    location : str
        The location to be checked.

    Returns
    -------
    bool
        True if the location is a valid city or country, False otherwise.
    """
    is_loc_a_city = location.lower() in CITIES
    is_loc_a_country = location.lower() in COUNTRIES
    return is_loc_a_city or is_loc_a_country


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
        openai.Completion.create(
            engine='davinci',
            prompt='Hello, World!',
            max_tokens=5
        )
    except openai.error.InvalidRequestError:
        return False
    except openai.error.AuthenticationError:
        return False

    return True


def is_departure_before_return(departure_date: datetime.date, return_date: datetime.date) -> bool:
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


def get_score_map(travel_plan_json: TravelPlanJSON) -> Dict[str, Dict[str, Union[float, int]]]:
    """

    """
    zs_classifier = classifier.ZeroShotTextClassifier(True)
    score_container = TravelPlanScore()
    scorer_obj = ActivitiesDiversityScorer(text_classifier=zs_classifier)
    scorer_obj.score(
        travel_plan=travel_plan_json,
        travel_plan_scores=score_container
    )

    return score_container.score_map
