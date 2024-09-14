import datetime
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class Activity(BaseModel):
    """Travel Plan Activity"""

    time: datetime.datetime = Field(
        description="Approximate time of the activity. The format should be YYYY-MM-DD HH:MM:SS"
    )
    place: str = Field(description="Name of the place where is located the activity")
    description: str = Field(description="Description of the activity")


class DayPlan(BaseModel):
    """Plan of a day in the travel plan"""

    date: datetime.date = Field(description="Date of the plan")
    activities: List[Activity] = Field(
        description="List of activities to do in the day plan."
    )
    city: str = Field(description="Name of the city where i located the day plan")


class TravelPlan(BaseModel):
    """Travel Plan"""

    day_plans: List[DayPlan] = Field(description="List of day plans activities")
