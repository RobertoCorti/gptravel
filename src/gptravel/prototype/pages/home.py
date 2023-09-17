from datetime import datetime

import streamlit as st

from gptravel.core.io.loggerconfig import logger
from gptravel.prototype import help as prototype_help
from gptravel.prototype import utils as prototype_utils
from gptravel.prototype.objects import geo_decoder
from gptravel.prototype.pages import travel as travel_page


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
    travel_reason_strp = travel_reason.strip()
    input_options = {
        "openai_key": openai_key,
        "departure_date": departure_date,
        "return_date": return_date,
        "departure": departure,
        "destination": destination,
        "travel_reason": None if travel_reason_strp == "" else travel_reason_strp,
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
    departure_date: datetime,
    return_date: datetime,
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
    departure_date : datetime
        Departure date.
    return_date : datetime
        Return date.
    openai_key : str
        OpenAI API key.

    Returns
    -------
    bool
        True if the input parameters are valid, False otherwise.
    """
    if (not geo_decoder.is_location_country_city_state(departure)) or (
        not geo_decoder.is_location_country_city_state(destination)
    ):
        warn_message = "Travel destination or/and departure is not valid."
        st.sidebar.warning(warn_message)
        logger.warning(warn_message)
        return False
    if not prototype_utils.is_departure_before_return(
        departure_date=departure_date, return_date=return_date
    ):
        warn_message = (
            "Travel dates are not correct. Departure should be before return."
        )
        st.sidebar.warning(warn_message)
        logger.warning(warn_message)
        return False
    if not prototype_utils.is_valid_openai_key(openai_key):
        warn_message = "Not valid OpenAI API Access Key"
        st.sidebar.warning(warn_message)
        logger.warning(warn_message)
        return False

    return True
