import datetime
from typing import Any, Dict

import streamlit as st
import pycountry
import allcities

from gptravel.app import utils

COUNTRIES = (country.name.lower() for country in pycountry.countries)
CITIES = (city.name.lower() for city in allcities.cities)


@st.cache_data
def _get_travel_plan(openai_key: str,
                     departure: str, destination: str,
                     departure_date: datetime.datetime, return_date: datetime.datetime,
                     travel_reason: str) -> Dict[str, Any]:
    ## compute input params
    n_days = (return_date - departure_date).days

    travel_parameters = dict(departure_place=departure, destination_place=destination,
                             n_travel_days=n_days, travel_theme=travel_reason)

    ## create plan
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
    st.title("GPTravel")

    openai_key = st.sidebar.text_input("OpenAI API Key",
                                       help="Enter you OpenAI key",
                                       placeholder="Enter your OpenAI key here")

    departure_date = st.sidebar.date_input("Select a date")
    return_date = st.sidebar.date_input(key="return_date", label="Select a return date")
    departure = st.sidebar.text_input(label="Departure", placeholder="Select a departure")
    destination = st.sidebar.text_input(label="Destination", placeholder="Select a destination")

    travel_reason = st.sidebar.selectbox("Select a travel reason",
                                         ["", "Business", "Romantic", "Solo", "Friends", "Family"])

    input_options = dict(openai_key=openai_key, departure_date=departure_date, return_date=return_date,
                         departure=departure, destination=destination,
                         travel_reason=None if travel_reason == '' else travel_reason)

    if st.sidebar.button("Let's go!"):
        if _is_valid_input(openai_key=openai_key,
                           departure_date=departure_date, return_date=return_date,
                           departure=departure, destination=destination):
            with st.spinner('Wait for it...'):
                travel_plan_dict = _get_travel_plan(**input_options)
                travel_plan_page(travel_plan_dict=travel_plan_dict, departure_date=departure_date, return_date=return_date)


def _is_valid_input(departure: str, destination: str,
                    departure_date: datetime.datetime, return_date: datetime.datetime,
                    openai_key: str) -> bool:
    if (departure.lower() not in CITIES and departure.lower() not in COUNTRIES) or (
            destination.lower() not in CITIES and destination.lower() not in COUNTRIES):
        st.sidebar.warning("Travel destination or/and departure is not valid.")
        st.markdown(f"{departure.lower()} not in CITIES: {departure.lower() not in CITIES}")
        st.markdown(f"{departure.lower()}not in COUNTRIES: {departure.lower() not in COUNTRIES}")
        return False
    if departure_date >= return_date:
        st.sidebar.warning("Travel dates are not correct. Departure should be before return.")
        return False
    if openai_key == '':
        ### TODO (RC): check if the api key is a real one
        st.sidebar.warning("Not valid OpenAI API Access Key")
        return False

    return True


if __name__ == "__main__":
    main()
