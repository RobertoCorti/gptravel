import datetime
from enum import Enum
from typing import List, Union

from langchain_core.pydantic_v1 import BaseModel, Field

DEPARTURE_ID_DESCRIPTION = """Parameter defines the departure airport code or location kgmid.
An airport code is an uppercase 3-letter code. You can search for it on Google Flights or IATA.
For example, CDG is Paris Charles de Gaulle Airport and AUS is Austin-Bergstrom International Airport.
A location kgmid is a string that starts with /m/. You can search for a location on Wikidata and use its "Freebase ID" as the location kgmid. For example, /m/0vzm is the location kgmid for Austin, TX.
You can specify multiple departure airports by separating them with a comma. For example, CDG,ORY,/m/04jpl
"""

ARRIVAL_ID_DESCRIPTION = """Parameter defines the arrival airport code or location kgmid.
An airport code is an uppercase 3-letter code. You can search for it on Google Flights or IATA.
For example, CDG is Paris Charles de Gaulle Airport and AUS is Austin-Bergstrom International Airport.
A location kgmid is a string that starts with /m/. You can search for a location on Wikidata and use its "Freebase ID" as the location kgmid. For example, /m/0vzm is the location kgmid for Austin, TX.
You can specify multiple arrival airports by separating them with a comma. For example, CDG,ORY,/m/04jpl
"""


class FlightClass(Enum):
    economy = "economy"
    premium_economy = "premium-economy"
    business = "business"
    first = "first"


TRAVEL_CLASS_MAP = {
    FlightClass.economy: 1,
    FlightClass.premium_economy: 2,
    FlightClass.business: 3,
    FlightClass.first: 4,
}


class FlightSearchParameters(BaseModel):
    """Flight Search parameters"""

    departure_id: str = Field(description=DEPARTURE_ID_DESCRIPTION)
    arrival_id: str = Field(description=ARRIVAL_ID_DESCRIPTION)
    travel_class: FlightClass = Field(
        description="The travel class of the flight. (example: economy, premium-economy, business, or first)",
        default="economy",
    )
    date: datetime.date = Field(description="Date of the flight")


class ItineraryFlightSearchParameters(BaseModel):
    """Search Inputs for Travel"""

    itinerary_flight_search_input: List[FlightSearchParameters] = Field(
        description="itinerary flight search parameters"
    )


class Airport(BaseModel):
    name: str = Field(description="The name of the airport.")
    airport_id: str = Field(
        description="The unique identifier (IATA code) of the airport."
    )
    time: str = Field(description="The scheduled time of departure or arrival.")


class Flight(BaseModel):
    departure_airport: Airport = Field(description="The departure airport details.")
    arrival_airport: Airport = Field(description="The arrival airport details.")
    duration: int = Field(description="Duration of the flight in minutes.")
    airline: str = Field(description="The airline operating the flight.")
    travel_class: FlightClass = Field(description="The travel class of the flight.")
    flight_number: str = Field(description="The flight number assigned by the airline.")
    price: Union[int, float] = Field(
        description="The price of the flight in the specified currency."
    )
    reason: str = Field(
        description="The reason for having chosen this flight for the travel plan"
    )


class FlightDetails(BaseModel):
    flights: List[Flight] = Field(
        description="A list of flight segments included in this itinerary."
    )
