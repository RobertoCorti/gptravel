import datetime

import allcities
import pycountry
import streamlit as st

from gptravel.prototype import help as prototype_help
from gptravel.prototype import utils as prototype_utils
from gptravel.prototype.pages import travel as travel_page

COUNTRIES = (country.name.lower() for country in pycountry.countries)
CITIES = (city.name.lower() for city in allcities.cities)


def main():
    """
    Main function for running GPTravel.

    It allows users to input travel parameters and generates a travel plan when the "Let's go!" button is clicked.
    """
    st.title("GPTravel ✈️")
    st.write("\n\n")

    openai_key = st.sidebar.text_input(
        "OpenAI API Key",
        help=prototype_help.OPENAI_KEY_HELP,
        placeholder="Enter your OpenAI key here",
    )

    departure_date = st.sidebar.date_input(
        "Select a date", help=prototype_help.DEPARTURE_DATE_HELP
    )

    return_date = st.sidebar.date_input(
        label="Select a return date",
        key="return_date",
        help=prototype_help.RETURN_DATE_HELP,
    )

    departure = st.sidebar.text_input(
        label="Departure",
        placeholder="Select a departure",
        help=prototype_help.DEPARTURE_LOC_HELP,
    )

    destination = st.sidebar.text_input(
        label="Destination",
        placeholder="Select a destination",
        help=prototype_help.DESTINATION_LOC_HELP,
    )

    travel_reason = st.sidebar.selectbox(
        "Select a travel reason",
        options=["", "Business", "Romantic", "Solo", "Friends", "Family"],
        help=prototype_help.TRAVEL_REASON_HELP,
    )

    input_options = {
        "openai_key": openai_key,
        "departure_date": departure_date,
        "return_date": return_date,
        "departure": departure,
        "destination": destination,
        "travel_reason": None if travel_reason == "" else travel_reason,
    }

    if st.sidebar.button("Let's go!"):
        if _is_valid_input(
            openai_key=openai_key,
            departure_date=departure_date,
            return_date=return_date,
            departure=departure,
            destination=destination,
        ):
            with st.spinner("Preparing your travel plan..."):
                travel_page.main(**input_options)


def _is_valid_input(
    departure: str,
    destination: str,
    departure_date: datetime.datetime,
    return_date: datetime.datetime,
    openai_key: str,
) -> bool:
    """
    Check if the input parameters are valid.

    Parameters
    ----------
    departure : str
        Departure location.
    destination : str
        Destination location.
    departure_date : datetime.datetime
        Departure date.
    return_date : datetime.datetime
        Return date.
    openai_key : str
        OpenAI API key.

    Returns
    -------
    bool
        True if the input parameters are valid, False otherwise.
    """
    if (not prototype_utils.is_valid_location(departure)) or (
        not prototype_utils.is_valid_location(destination)
    ):
        st.sidebar.warning("Travel destination or/and departure is not valid.")
        return False
    if not prototype_utils.is_departure_before_return(
        departure_date=departure_date, return_date=return_date
    ):
        st.sidebar.warning(
            "Travel dates are not correct. Departure should be before return."
        )
        return False
    if not prototype_utils.is_valid_openai_key(openai_key):
        st.sidebar.warning("Not valid OpenAI API Access Key")
        return False

    return True
