import datetime

import streamlit as st
import pycountry
import allcities

COUNTRIES = (country.name.lower() for country in pycountry.countries)
CITIES = (city.name.lower() for city in allcities.cities)


def travel_plan(departure, destination, departure_date, return_date, travel_reason):
    st.markdown("TRAVEL PLAN ACTIVATED")


def main():
    st.title("GPTravel")
    st.subheader("Your personal travel assistant")

    openai_key = st.sidebar.text_input("OpenAI API Key", placeholder="Enter your OpenAI key here")

    departure_date = st.sidebar.date_input("Select a date")
    return_date = st.sidebar.date_input(key="return_date", label="Select a return date")
    departure = st.sidebar.text_input(label="Departure", placeholder="Select a departure")
    destination = st.sidebar.text_input(label="Destination", placeholder="Select a destination")

    travel_reason = st.sidebar.selectbox("Select a travel reason",
                                         ["", "Business", "Romantic", "Solo", "Friends", "Family"])

    input_options = dict(openai_key=openai_key, departure_date=departure_date, return_date=return_date,
                         departure=departure, destination=destination, travel_reason=travel_reason)

    if st.sidebar.button("Let's go!"):
        if _is_valid_input(**input_options):
            travel_plan(**input_options)


def _is_valid_input(departure: str, destination: str,
                    departure_date: datetime.datetime, return_date: datetime.datetime,
                    openai_key: str, travel_reason: str) -> None:
    if (departure.lower() not in CITIES) or (departure.lower() not in COUNTRIES) or (
            destination.lower() not in CITIES) or (destination.lower() not in COUNTRIES):
        st.sidebar.warning("Travel destination or/and departure is not valid.")
    if departure_date >= return_date:
        st.sidebar.warning("Travel dates are not correct. Departure should be before return.")
    if openai_key == '':
        st.sidebar.warning("Not valid OpenAI API Access Key")
    else:
        travel_plan(departure, destination, departure_date, return_date, travel_reason)


if __name__ == "__main__":
    main()
