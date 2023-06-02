import datetime
import os
from typing import Any, Dict

import streamlit as st
import pycountry
import allcities

from gptravel.app import utils
from gptravel.prototype import utils as prototype_utils
from gptravel.prototype import help

COUNTRIES = (country.name.lower() for country in pycountry.countries)
CITIES = (city.name.lower() for city in allcities.cities)

st.set_page_config(page_title="GPTravel", page_icon="✈️")


@st.cache_data(show_spinner=False)
def _get_travel_plan(openai_key: str,
                     departure: str, destination: str,
                     departure_date: datetime.datetime, return_date: datetime.datetime,
                     travel_reason: str) -> Dict[str, Any]:
    os.environ['OPENAI_API_KEY'] = openai_key
    n_days = (return_date - departure_date).days

    travel_parameters = dict(departure_place=departure, destination_place=destination,
                             n_travel_days=n_days, travel_theme=travel_reason)

    prompt = utils.build_prompt(travel_parameters)
    travel_plan_json = utils.get_travel_plan_json(prompt)
    travel_plan_dict = travel_plan_json.travel_plan

    return travel_plan_dict


def travel_plan_page(travel_plan_dict, departure_date, return_date):
    for day_num, (day_key, places_dict) in enumerate(travel_plan_dict.items()):
        date_str = (departure_date + datetime.timedelta(days=int(day_num))).strftime("%d-%m-%Y")
        expander_day_num = st.expander(f"{day_key} ({date_str})", expanded=True)
        for place, activities in places_dict.items():
            expander_day_num.markdown(f"**{place}**")
            for activity in activities:
                expander_day_num.markdown(f"- {activity}")


def main():
    st.title("GPTravel ✈️")
    st.write("\n\n")

    openai_key = st.sidebar.text_input(
        "OpenAI API Key",
        help=help.OPENAI_KEY_HELP,
        placeholder="Enter your OpenAI key here"
    )

    departure_date = st.sidebar.date_input(
        "Select a date",
        help=help.DEPARTURE_DATE_HELP
    )

    return_date = st.sidebar.date_input(
        label="Select a return date",
        key="return_date",
        help=help.RETURN_DATE_HELP
    )

    departure = st.sidebar.text_input(
        label="Departure",
        placeholder="Select a departure",
        help=help.DEPARTURE_LOC_HELP
    )

    destination = st.sidebar.text_input(
        label="Destination",
        placeholder="Select a destination",
        help=help.DESTINATION_LOC_HELP
    )

    travel_reason = st.sidebar.selectbox("Select a travel reason",
                                         options=["", "Business", "Romantic", "Solo", "Friends", "Family"],
                                         help=help.TRAVEL_REASON_HELP)

    input_options = dict(openai_key=openai_key, departure_date=departure_date, return_date=return_date,
                         departure=departure, destination=destination,
                         travel_reason=None if travel_reason == '' else travel_reason)

    if st.sidebar.button("Let's go!"):
        if _is_valid_input(openai_key=openai_key,
                           departure_date=departure_date, return_date=return_date,
                           departure=departure, destination=destination):
            with st.spinner('Preparing your travel plan...'):
                travel_plan_dict = _get_travel_plan(**input_options)
                travel_plan_page(travel_plan_dict=travel_plan_dict, departure_date=departure_date,
                                 return_date=return_date)


def is_departure_before_return(departure_date: datetime.date, return_date: datetime.date) -> bool:
    return departure_date >= return_date


def _is_valid_input(departure: str, destination: str,
                    departure_date: datetime.datetime, return_date: datetime.datetime,
                    openai_key: str) -> bool:
    if (not prototype_utils.is_valid_location(departure)) or (not prototype_utils.is_valid_location(destination)):
        st.sidebar.warning("Travel destination or/and departure is not valid.")
        st.markdown(f"{departure.lower()} not in CITIES: {departure.lower() not in CITIES}")
        st.markdown(f"{departure.lower()}not in COUNTRIES: {departure.lower() not in COUNTRIES}")
        return False
    if not prototype_utils.is_departure_before_return:
        st.sidebar.warning("Travel dates are not correct. Departure should be before return.")
        return False
    if not prototype_utils.is_valid_openai_key(openai_key):
        st.sidebar.warning("Not valid OpenAI API Access Key")
        return False

    return True


if __name__ == "__main__":
    main()
