import streamlit as st
import airportsdata

airports = airportsdata.load()


def travel_plan(airports, departure_airport, arrival_airport, departure_date, return_date, travel_reason, openai_key):
    ## clean current page

    st.empty()


def main():
    st.title("GPTravel")
    st.subheader("Your personal travel assistant")

    st.sidebar.subheader("About")
    about = st.sidebar.markdown("GPTravel is a personal travel assistant that helps you plan your next trip. "
                                "It uses the power of OpenAI's GPT-3 to generate a travel plan based on your preferences. "
                                "It is currently a prototype, so it is not perfect yet. ")

    openai_key = st.sidebar.text_input("OpenAI Key", placeholder="Enter your OpenAI key here")

    departure_date = st.date_input("Select a date")
    return_date = st.date_input(key="return_date", label="Select a return date")

    airport_cities = sorted(set(f"{v['city']} ({v['country']})" for v in airports.values() if len(v['city']) != 0))
    departure_airport = st.selectbox("Select a departure airport", airport_cities)
    arrival_airport = st.selectbox("Enter an arrival airport", airport_cities)

    travel_reason = st.selectbox("Select a travel reason", ["Business", "Romantic", "Solo", "Friends", "Family"])

    if st.button("Let's go!"):
        travel_plan(airports, departure_airport, arrival_airport, departure_date, return_date, travel_reason,
                    openai_key)


if __name__ == "__main__":
    main()
