import datetime
from typing import List, Optional, Union

from langchain_core.pydantic_v1 import BaseModel, Field, conint


class HotelSearchParameters(BaseModel):
    """Hotel Search parameters"""

    q: str = Field(
        description="Parameter defines the city of the accodomation. You can use anything that you would use in a regular Google Hotels search."
    )
    check_in_date: datetime.date = Field(
        description="Parameter defines the check-in date. The format is YYYY-MM-DD. e.g. 2024-08-31"
    )
    check_out_date: datetime.date = Field(
        description="Parameter defines the check-out date. The format is YYYY-MM-DD. e.g. 2024-09-01"
    )
    adults: Optional[int] = Field(
        description="Parameter defines the number of adults. Default to 2."
    )
    children: Optional[int] = Field(
        description="Parameter defines the number of children. Default to 0."
    )
    children_ages: Optional[List[int]] = Field(
        description="Parameter defines the ages of children. The age range is from 1 to 17, with children who haven't reached 1 year old being considered as 1. Example for single child only 5. Example for multiple children (seperated by comma ,): [5,8,10]"
    )
    max_price: Optional[int] = Field(
        description="Parameter defines the upper bound of price range."
    )


class HotelSearchInputs(BaseModel):
    """Search Inputs for Travel accomodations"""

    search_list: List[HotelSearchParameters] = Field(
        description="List of hotel search parameters for each travel night"
    )


class GpsCoordinates(BaseModel):
    latitude: float = Field(description="The latitude coordinate of the accomodation.")
    longitude: float = Field(
        description="The longitude coordinate of the accomodation."
    )
    city: str = Field(description="City of the accomodation.")


class Rate(BaseModel):
    lowest: str = Field(
        description="The lowest rate displayed as a string (including currency symbol)."
    )
    extracted_lowest: Union[int, float] = Field(
        description="The extracted lowest rate as a numerical value."
    )
    before_taxes_fees: str = Field(
        description="The rate before taxes and fees, displayed as a string (including currency symbol)."
    )
    extracted_before_taxes_fees: Union[int, float] = Field(
        description="The extracted rate before taxes and fees as a numerical value."
    )


class Transportation(BaseModel):
    type_: str = Field(description="Type of transportation (e.g., Taxi, Walking).")
    duration: str = Field(
        description="Estimated duration for the transportation option."
    )


class NearbyPlace(BaseModel):
    name: str = Field(description="Name of the nearby place.")
    transportations: List[Transportation] = Field(
        description="Available transportation options and their durations to the place."
    )


class Rating(BaseModel):
    stars: conint(ge=1, le=5) = Field(
        description="The number of stars given in the rating."
    )
    count: int = Field(description="The number of reviews that gave this star rating.")


class ReviewsBreakDown(BaseModel):
    name: str = Field(description="Name of the review category.")
    description: str = Field(description="Description of the review category.")
    total_mentioned: str = Field(
        description="Total number of reviews of the category (positive, neutral and negative)."
    )
    positive: int = Field(description="Number of positive reviews.")
    neutral: int = Field(description="Number of neutral reviews.")
    negative: int = Field(description="Number of negative reviews.")


class HotelDetails(BaseModel):
    type: str = Field(description="The type of accomodation (for example hotel).")
    name: str = Field(description="The name of the hotel.")
    description: str = Field(description="A brief description of the hotel.")
    link: Optional[str] = Field(
        description="web url of the main page of the hotel.", default="unknown"
    )
    gps_coordinates: GpsCoordinates = Field(
        description="The GPS coordinates (latitude and longitude) of the hotel."
    )
    check_in_time: str = Field(description="The check-in time at the hotel.")
    check_out_time: str = Field(description="The check-out time at the hotel.")
    rate_per_night: Rate = Field(
        description="Details about the rate per night, including lowest rates and rates before taxes and fees."
    )
    total_rate: Rate = Field(
        description="Total rate details for the stay, including lowest rates and rates before taxes and fees."
    )
    nearby_places: List[NearbyPlace] = Field(
        description="A list of places nearby the hotel, with available transportation options."
    )
    hotel_class: Optional[str] = Field(
        description="The class of the hotel (e.g., 1-star tourist hotel).",
        default="unknown",
    )
    overall_rating: float = Field(description="The overall rating of the hotel.")
    reviews: int = Field(description="The total number of reviews for the hotel.")
    reviews_breakdown: Optional[List[ReviewsBreakDown]] = Field(
        description="Reviews breakdown for different categories."
    )
    ratings: List[Rating] = Field(description="A breakdown of ratings by star count.")
    location_rating: float = Field(description="The rating of the hotel's location.")
    amenities: List[str] = Field(
        description="A list of amenities provided by the hotel (e.g., Free Wi-Fi, Pet-friendly)."
    )
    reason: str = Field(
        description="The reason for having chosen this accomodation for the travel plan"
    )


class AccomodationstDetails(BaseModel):
    accomodations: List[HotelDetails] = Field(
        description="A list of the best accomodations, one (unless specified by the user contrary) for each city visited by the user in the travel plan."
    )
