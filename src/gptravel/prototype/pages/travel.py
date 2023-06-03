import os
import datetime
from typing import Any, Dict, Tuple, Union
import streamlit as st
import plotly.graph_objects as go
from plotly.graph_objs import Figure

from gptravel.prototype import style as prototype_style
from gptravel.app import utils
from gptravel.prototype import utils as prototype_utils


def main(openai_key: str,
         departure: str, destination: str,
         departure_date: datetime.datetime, return_date: datetime.datetime,
         travel_reason: str):
    """
     Main function for running travel plan in GPTravel.
     It generates a travel page and display all functionalities of the page.

    Parameters
    ----------
    openai_key : str
        OpenAI API key.
    departure : str
        Departure place.
    destination : str
        Destination place.
    departure_date : datetime.datetime
        Departure date.
    return_date : datetime.datetime
        Return date.
    travel_reason : str
        Reason for travel.
    """
    travel_plan_dict, score_dict = _get_travel_plan(openai_key=openai_key,
                                                    departure=departure, destination=destination,
                                                    departure_date=departure_date, return_date=return_date,
                                                    travel_reason=travel_reason)
    _create_expanders_travel_plan(departure_date, score_dict, travel_plan_dict)


@st.cache_data(show_spinner=False)
def _get_travel_plan(openai_key: str,
                     departure: str, destination: str,
                     departure_date: datetime.datetime,
                     return_date: datetime.datetime,
                     travel_reason: str) \
        -> Tuple[Dict[Any, Any], Dict[str, Dict[str, Union[float, int]]]]:
    """
    Get the travel plan and score dictionary.

    Parameters
    ----------
    openai_key : str
        OpenAI API key.
    departure : str
        Departure place.
    destination : str
        Destination place.
    departure_date : datetime.datetime
        Departure date.
    return_date : datetime.datetime
        Return date.
    travel_reason : str
        Reason for travel.

    Returns
    -------
    Tuple[Dict[Any, Any], Dict[str, Dict[str, Union[float, int]]]]
        A tuple containing the travel plan dictionary and the score dictionary.
    """
    os.environ['OPENAI_API_KEY'] = openai_key
    n_days = (return_date - departure_date).days

    travel_parameters = {
        "departure_place": departure,
        "destination_place": destination,
        "n_travel_days": n_days,
        "travel_theme": travel_reason
    }

    prompt = utils.build_prompt(travel_parameters)
    travel_plan_json = utils.get_travel_plan_json(prompt)
    travel_plan_dict = travel_plan_json.travel_plan

    score_dict = prototype_utils.get_score_map(travel_plan_json)

    return travel_plan_dict, score_dict


def _create_expanders_travel_plan(departure_date, score_dict, travel_plan_dict):
    """
    Create expanders for displaying the travel plan.

    Parameters
    ----------
    departure_date : datetime.datetime
        Departure date.
    score_dict : Dict[str, Any]
        Score dictionary.
    travel_plan_dict : Dict[Any, Any]
        Travel plan dictionary.
    """
    for day_num, (day_key, places_dict) in enumerate(travel_plan_dict.items()):
        date_str = (departure_date + datetime.timedelta(days=int(day_num))).strftime("%d-%m-%Y")
        expander_day_num = st.expander(f"{day_key} ({date_str})", expanded=True)
        for place, activities in places_dict.items():
            expander_day_num.markdown(f"**{place}**")
            for activity in activities:
                activity_descr = f" {activity}"
                filtered_activities = filter(lambda x: x[1] > .5,
                                             score_dict['Activities Variety']['labeled_activities'][activity].items())
                sorted_filtered_activities = sorted(filtered_activities, key=lambda x: x[1], reverse=True)
                activity_label = " ".join(
                    f'<span style="background-color:{prototype_style.COLOR_LABEL_ACTIVITY_DICT[label]}; {prototype_style.LABEL_BOX_STYLE}">\t\t<b>{label.upper()}</b></span>'
                    for label, _ in sorted_filtered_activities)
                expander_day_num.markdown(f"- {activity_label} {activity_descr}\n", unsafe_allow_html=True)


def _get_score_pie_chart(score_dict: Dict[str, Any]) -> Figure:
    """
    Generate a pie chart for the score distribution.

    Parameters
    ----------
    score_dict : Dict[str, Any]
        Score dictionary.

    Returns
    -------
    Figure
        The generated pie chart.
    """
    labels = []
    values = []
    colors = []

    for key, value in score_dict['Activities Variety']['activities_distribution'].items():
        if key in prototype_style.COLOR_LABEL_ACTIVITY_DICT:
            labels.append(key)
            values.append(value)
            colors.append(prototype_style.COLOR_LABEL_ACTIVITY_DICT[key])

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.75,
                                 marker={"colors": colors},
                                 hovertemplate='<b>%{label}</b><br>%{percent:.2f}%<extra></extra>')])

    return fig
