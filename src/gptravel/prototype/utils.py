"""
utils.py

A module that provides utility functions for streamlit app.

Dependencies:
- pycountry
- allcities

Module-level constants:
- COUNTRIES: A list of lowercase country names.
- CITIES: A list of lowercase city names.

Functions:
- is_valid_location(location: str) -> bool:
    Check if a location is valid.

    Parameters:
    - location (str): The location to be checked.

    Returns:
    - bool: True if the location is a valid city or country, False otherwise.
"""

import pycountry
import allcities

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
