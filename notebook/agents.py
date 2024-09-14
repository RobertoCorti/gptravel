import datetime
import json
from copy import copy
from operator import itemgetter
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from accomodations_schema import AccomodationstDetails, HotelDetails, HotelSearchInputs
from flights_schema import (
    TRAVEL_CLASS_MAP,
    FlightDetails,
    ItineraryFlightSearchParameters,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableAssign, RunnableLambda, RunnableMap
from langchain_core.runnables.base import RunnableSequence
from langchain_openai import ChatOpenAI
from serpapi import GoogleSearch
from travel_plan_schema import TravelPlan


def get_travel_plan_generation_prompt(
    input_parameters: Dict[str, Any]
) -> PromptTemplate:
    additional_text = ""
    additional_text_1 = ""
    prompt_input_variables = ["destination_place", "departure_date", "return_date"]
    if input_parameters.get("user_travel_notes", "").strip() != "":
        additional_text += '\nIn addition to that the user expressed this preference for her/his travel: "{user_travel_notes}".'
        additional_text_1 += ", even if expressed inside the user's preferences"
        prompt_input_variables.append("user_travel_notes")

    travel_plan_prompt_generation_template = (
        """You are an intelligent travel planner.
    
The user is interested to travel to {destination_place} between {departure_date} and {return_date}."""
        + additional_text
        + """
With this in mind, generate a JSON that could contain a travel plan that could match user interests.
In the travel plan, please avoid activities related to flights and transports, also everything included about the accomodation"""
        + additional_text_1
        + """.
Just tell what to do when the user is at destination.
    """
    )
    return PromptTemplate(
        template=travel_plan_prompt_generation_template,
        input_variables=prompt_input_variables,
    )


def get_travel_plan_generator_agent(
    input_parameters: Dict[str, Any]
) -> RunnableSequence:
    local_parameters = copy(input_parameters)
    local_parameters["gpt_params"]["model"] = "gpt-4o"
    llm_travel_plan_generator = ChatOpenAI(
        **local_parameters["gpt_params"]
    ).with_structured_output(TravelPlan)

    prompt_travel_plan_generator = get_travel_plan_generation_prompt(
        input_parameters=local_parameters
    )
    return prompt_travel_plan_generator | llm_travel_plan_generator


def extract_from_travel_plan_city_itinerary(
    travel_plan: TravelPlan, departure_place: str
) -> List[Dict[str, Union[Tuple[str, str], datetime.date]]]:
    itinerary_list = []
    previous_city = departure_place
    for i, day_plan in enumerate(travel_plan.day_plans):
        if day_plan.city != previous_city:
            itinerary_list.append(
                {"itinerary": (previous_city, day_plan.city), "date": day_plan.date}
            )
            previous_city = day_plan.city
    itinerary_list.append(
        {
            "itinerary": (previous_city, departure_place),
            "date": travel_plan.day_plans[-1].date,
        }
    )
    return itinerary_list


def extract_best_flights_from_api_response(
    api_response: Dict[str, Any], index_offset: int = 0
) -> List[Dict[str, Any]]:
    try:
        best_flights = api_response["best_flights"]
    except KeyError:
        best_flights = api_response["other_flights"]
    return [
        {
            "flight_id": i + index_offset,
            "departure_time": x["flights"][0]["departure_airport"]["time"],
            "arrival_time": x["flights"][0]["arrival_airport"]["time"],
            "departure_airport": x["flights"][0]["departure_airport"]["name"],
            "arrival_airport": x["flights"][0]["arrival_airport"]["name"],
            "airline": x["flights"][0]["airline"],
            "price": x["price"],
            "total_duration": x["total_duration"],
        }
        for i, x in enumerate(best_flights)
    ]


def get_flights_json(
    travel_itinerary: ItineraryFlightSearchParameters,
    serp_api_default_pars: Dict[str, Any],
    json_endpoint: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    best_flight_result = []
    for i, itinerary in enumerate(travel_itinerary.itinerary_flight_search_input):
        n = len(best_flight_result)
        search_pars = {
            "departure_id": itinerary.departure_id,
            "arrival_id": itinerary.arrival_id,
            "outbound_date": itinerary.date.strftime("%Y-%m-%d"),
            "travel_class": TRAVEL_CLASS_MAP[itinerary.travel_class],
        }
        search_pars.update(serp_api_default_pars)
        flight_search = None
        if json_endpoint is None:
            print("Fetching from SERPAPI")
            flight_search = GoogleSearch(search_pars).get_dict()
        else:
            print("Reading from direct endpoint")
            endpoint = json_endpoint[i]
            flight_search = requests.get(endpoint).json()

        best_flight_result += extract_best_flights_from_api_response(
            api_response=flight_search, index_offset=n
        )
    return best_flight_result


def get_flight_query_agent(
    input_parameters: Dict[str, Any],
    serp_api_default_pars: Dict[str, Any],
    hardcoded_endpoints: Optional[List[str]] = None,
) -> RunnableSequence:
    itinerary_list_lambda = RunnableLambda(
        lambda x: extract_from_travel_plan_city_itinerary(
            travel_plan=x["generated_travel_plan"], departure_place=x["departure_place"]
        )
    )
    prompt_flight_query_template = """You are an intelligent travel planner.

You are provided with the following flight itinerary list: {flight_itinerary_list}. 

Given this in mind, we need to get the information required for calling SerpAPI for the search flights. 
    """
    flight_query_prompt = PromptTemplate(
        template=prompt_flight_query_template, input_variables=["flight_itinerary_list"]
    )
    local_parameters = copy(input_parameters)
    local_parameters["gpt_params"]["model"] = "gpt-4o-mini"

    llm_flight_query = ChatOpenAI(
        **local_parameters["gpt_params"]
    ).with_structured_output(ItineraryFlightSearchParameters)

    itinerary_list_getter = (
        RunnableMap(
            {
                "generated_travel_plan": itemgetter("generated_travel_plan"),
                "departure_place": itemgetter("departure_place"),
            }
        )
        | itinerary_list_lambda
    )

    itinerary_list_generator_agent = (
        {"flight_itinerary_list": itinerary_list_getter}
        | flight_query_prompt
        | llm_flight_query
    )

    flight_list_api_getter_agent = itemgetter(
        "generated_tp_flight_itinerary"
    ) | RunnableLambda(
        lambda x: get_flights_json(
            travel_itinerary=x,
            serp_api_default_pars=serp_api_default_pars,
            json_endpoint=hardcoded_endpoints,
        )
    )
    return {
        "generated_tp_flight_itinerary": itinerary_list_generator_agent
    } | flight_list_api_getter_agent


def get_flights_selector_prompt(input_parameters: Dict[str, Any]) -> PromptTemplate:
    additional_text = ""
    additional_text_2 = ""
    additional_text_3 = ""
    prompt_input_variables = [
        "destination_place",
        "departure_date",
        "return_date",
        "departure_place",
        "generated_travel_plan_json",
        "available_flights",
    ]
    if input_parameters.get("user_travel_notes", "").strip() != "":
        additional_text += '\nThe user expressed these preferences for her/his travel: "{user_travel_notes}".'
        additional_text_2 = "(if the user has provided her/his preferences for the flights, you should assign to them the priority)"
        additional_text_3 = "\nIf the users preferences cannot be satisfied by the available flights, select a reasonable one"
        prompt_input_variables.append("user_travel_notes")

    flight_agent_selector_prompt = (
        """You are an intelligent travel planner.

The user is interest to travel to {destination_place} between {departure_date} and {return_date} departing from {departure_place}.

In the previous iterations you created the following travel plan: {generated_travel_plan_json}.

You have checked the available flights for the travel itinerary and are the following ones: {available_flights}
"""
        + additional_text
        + """

Based on these information, you must select the best flights for the generated travel plan.
The general parameters to take into account should be"""
        + additional_text_2
        + """:
- Flight prices
"""
        + additional_text_3
    )
    return PromptTemplate(
        template=flight_agent_selector_prompt, input_variables=prompt_input_variables
    )


def get_flights_selector_agent(input_parameters: Dict[str, Any]) -> RunnableSequence:
    local_parameters = copy(input_parameters)
    local_parameters["gpt_params"]["model"] = "gpt-4o-mini"
    local_parameters["gpt_params"]["temperature"] = 0
    llm_flight_selector_agent = ChatOpenAI(
        **local_parameters["gpt_params"]
    ).with_structured_output(FlightDetails)

    prompt_travel_plan_generator = get_flights_selector_prompt(
        input_parameters=local_parameters
    )
    return prompt_travel_plan_generator | llm_flight_selector_agent


def get_flight_selection_chain(
    input_parameters: Dict[str, Any],
    serp_api_default_pars: Dict[str, Any],
    hardcoded_endpoints: Optional[List[str]] = None,
) -> RunnableSequence:
    flight_query_agent = get_flight_query_agent(
        input_parameters=input_parameters,
        serp_api_default_pars=serp_api_default_pars,
        hardcoded_endpoints=hardcoded_endpoints,
    )
    flights_selector_agent = get_flights_selector_agent(
        input_parameters=input_parameters
    )
    return (
        RunnableAssign({"available_flights": flight_query_agent})
        | flights_selector_agent
    )


def extract_travel_plan_cities_and_dates(
    travel_plan: TravelPlan,
) -> List[Dict[str, Union[Tuple[str, str], datetime.date]]]:
    itinerary_list = []
    previous_city = None
    start_date = None
    for i, day_plan in enumerate(travel_plan.day_plans):
        if i == 0:
            previous_city = day_plan.city
            start_date = day_plan.date
        else:
            if previous_city != day_plan.city:
                itinerary_list.append(
                    {
                        "city": previous_city,
                        "first_date": start_date,
                        "last_date": travel_plan.day_plans[i - 1].date,
                    }
                )
                start_date = day_plan.date
                previous_city = day_plan.city
    if len(itinerary_list) == 0:
        itinerary_list.append(
            {
                "city": previous_city,
                "first_date": start_date,
                "last_date": travel_plan.day_plans[-1].date,
            }
        )
    return itinerary_list


def extract_hotels_info(api_response_json: Dict[str, Any], city: str):
    return [
        {
            "hotel_id": x,
            "type": element.get("type"),
            "name": element.get("name"),
            "description": element.get("description", ""),
            "link": element.get("link", None),
            "gps_coordinates": element.get("gps_coordinates"),
            "city": city,
            "check_in_time": element.get("check_in_time"),
            "check_out_time": element.get("check_out_time"),
            "rate_per_night": element.get("rate_per_night"),
            "total_rate": element.get("total_rate"),
            "nearby_places": element.get("nearby_places"),
            "overall_rating": element.get("overall_rating"),
            "reviews": element.get("reviews", 0),
            "reviews_breakdown": element.get("reviews_breakdown"),
            "ratings": element.get("ratings"),
            "location_rating": element.get("location_rating"),
            "amenities": element.get("amenities"),
        }
        for x, element in enumerate(api_response_json["properties"])
    ]


def get_accomodations_json(
    accomodations_info: HotelSearchInputs,
    serp_api_default_pars: Dict[str, Any],
    json_endpoint: Optional[List[str]] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    search_accomodations_inputs = json.loads(accomodations_info.json())
    accomodation_search_list = []
    for i, queries in enumerate(search_accomodations_inputs["search_list"]):
        hotel_search_params = serp_api_default_pars | queries
        if json_endpoint is None:
            print("Fetching from SERPAPI")
            api_call = GoogleSearch(hotel_search_params).get_dict()
        else:
            print("Reading from direct endpoint")
            endpoint = json_endpoint[i]
            api_call = requests.get(endpoint).json()
        accomodation_search_list.append(
            extract_hotels_info(api_call, city=queries["q"])
        )
    return accomodation_search_list


def get_accomodations_query_agent(
    input_parameters: Dict[str, Any],
    serp_api_default_pars: Dict[str, Any],
    hardcoded_endpoints: Optional[List[str]] = None,
) -> RunnableSequence:
    accomodations_query_prompt = """You are an intelligent travel planner.

The user is going to follow this itinerary for her/his travel: {accomodations_itinerary_list}.
This is what the user expressed: "{user_travel_notes}".
Given this in mind, we need to get the information required for calling SerpAPI for the search hotel accomodations. 
For each city of the plan, give in output the search api requests. 
    """
    accomodations_query_prompt_template = PromptTemplate(
        template=accomodations_query_prompt,
        input_variables=["accomodations_itinerary_list", "user_travel_notes"],
    )
    local_parameters = copy(input_parameters)
    local_parameters["gpt_params"]["model"] = "gpt-4o-mini"
    local_parameters["gpt_params"]["temperature"] = 0

    llm_accomodations_query = ChatOpenAI(
        **local_parameters["gpt_params"]
    ).with_structured_output(HotelSearchInputs)

    cities_itinerary_list_lambda = RunnableLambda(
        lambda x: extract_travel_plan_cities_and_dates(travel_plan=x)
    )

    cities_itinerary_list_getter = (
        itemgetter("generated_travel_plan") | cities_itinerary_list_lambda
    )

    accomodations_serp_api_pars_getter_prompt = {
        "accomodations_itinerary_list": cities_itinerary_list_getter,
        "user_travel_notes": itemgetter("user_travel_notes"),
    } | accomodations_query_prompt_template

    accomodations_serp_api_pars_agent = (
        accomodations_serp_api_pars_getter_prompt | llm_accomodations_query
    )

    accomodations_list_api_caller_agent = itemgetter(
        "accomodations_serp_api_pars"
    ) | RunnableLambda(
        lambda x: get_accomodations_json(
            accomodations_info=x,
            serp_api_default_pars=serp_api_default_pars,
            json_endpoint=hardcoded_endpoints,
        )
    )
    return {
        "accomodations_serp_api_pars": accomodations_serp_api_pars_agent
    } | accomodations_list_api_caller_agent


def get_accomodations_selector_prompt(
    input_parameters: Dict[str, Any]
) -> PromptTemplate:
    additional_text = ""
    additional_text_2 = ""
    additional_text_3 = ""
    prompt_input_variables = [
        "destination_place",
        "departure_date",
        "return_date",
        "generated_travel_plan_json",
        "available_accomodations",
    ]
    if input_parameters.get("user_travel_notes", "").strip() != "":
        additional_text += '\nThe user expressed these preferences for her/his travel: "{user_travel_notes}".'
        additional_text_2 = "(if the user has provided her/his preferences for the accomodations, you should assign to them the priority)"
        additional_text_3 = "\nIf the users preferences cannot be satisfied by the available accomodations, select a reasonable one"
        prompt_input_variables.append("user_travel_notes")

    accomodations_agent_selector_prompt = (
        """You are an intelligent travel planner.

The user is interest to travel to {destination_place} between {departure_date} and {return_date}.

In the previous iterations you created the following travel plan composed by lists of activities for each day: {generated_travel_plan_json}.

You have checked on Google Hotels all possible accomodations for each travel day:: {available_accomodations}
"""
        + additional_text
        + """

Based on this information, you must select the best accomodation/hotel.
Remember: you must choose one unique accomodation per city present in the travel plan above, unless specified by the user. It's mandatory!
The general parameters to take into account should be"""
        + additional_text_2
        + """:
- Accomodation price
- Number of reviews and ratings from other travellers
- Distance from the attractions suggested in the travel plan
- Services / amenities offered by the building
"""
        + additional_text_3
    )
    return PromptTemplate(
        template=accomodations_agent_selector_prompt,
        input_variables=prompt_input_variables,
    )


def get_accomodations_selector_agent(
    input_parameters: Dict[str, Any]
) -> RunnableSequence:
    local_parameters = copy(input_parameters)
    local_parameters["gpt_params"]["model"] = "gpt-4o-mini"
    local_parameters["gpt_params"]["temperature"] = 0
    llm_accomodations_selector_agent = ChatOpenAI(
        **local_parameters["gpt_params"]
    ).with_structured_output(AccomodationstDetails)

    prompt_accomodations_selector = get_accomodations_selector_prompt(
        input_parameters=local_parameters
    )
    return prompt_accomodations_selector | llm_accomodations_selector_agent


def get_accomodation_selection_chain(
    input_parameters: Dict[str, Any],
    serp_api_default_pars: Dict[str, Any],
    hardcoded_endpoints: Optional[List[str]] = None,
) -> RunnableSequence:
    accomodation_query_agent = get_accomodations_query_agent(
        input_parameters=input_parameters,
        serp_api_default_pars=serp_api_default_pars,
        hardcoded_endpoints=hardcoded_endpoints,
    )
    accomodations_selector_agent = get_accomodations_selector_agent(
        input_parameters=input_parameters
    )
    return (
        RunnableAssign({"available_accomodations": accomodation_query_agent})
        | accomodations_selector_agent
    )
