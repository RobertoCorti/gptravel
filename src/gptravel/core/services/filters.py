from abc import ABC, abstractmethod

from gptravel.core.io.loggerconfig import logger
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class Filter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def filter(self, travel_plan: TravelPlanJSON) -> None:
        pass


class DeparturePlaceFilter(Filter):
    def filter(self, travel_plan: TravelPlanJSON) -> None:
        logger.debug("DeparturePlaceFilter: Start")
        departure_place = travel_plan.departure_place.lower()
        # if the departure place is present in the travel plan then remove it
        if departure_place in [city.lower() for city in travel_plan.travel_cities]:
            logger.debug("Found %s inside the travel plan", departure_place)
            day_depth = travel_plan.keys_map["day"]
            if day_depth == 0:
                days_to_drop = []
                for day in travel_plan.travel_plan.keys():
                    key_to_remove = [
                        city
                        for city in travel_plan.travel_plan[day].keys()
                        if city.lower() == departure_place
                    ]
                    if key_to_remove:
                        logger.debug(
                            "Removed %s from the travel plan for %s",
                            departure_place,
                            day,
                        )
                        del travel_plan.travel_plan[day][key_to_remove[0]]
                    # if the day container is empty then remove it
                    if travel_plan.travel_plan[day] == {}:
                        days_to_drop.append(day)
                        logger.debug("Removed %s completely from the travel plan", day)
                if days_to_drop:
                    for day_to_delete in days_to_drop:
                        del travel_plan.travel_plan[day_to_delete]
                    # fix the order of the
                    day_first_word = days_to_drop[0].split(" ")[0]
                    day_keys = list(travel_plan.travel_plan.keys())
                    n_day_counter = 1
                    for old_key in day_keys:
                        new_key = day_first_word + " " + str(n_day_counter)
                        travel_plan.travel_plan[new_key] = travel_plan.travel_plan.pop(
                            old_key
                        )
                        n_day_counter += 1
            else:
                key_to_remove = [
                    city
                    for city in travel_plan.travel_plan.keys()
                    if city.lower() == departure_place
                ][0]
                del travel_plan.travel_plan[key_to_remove]
        logger.debug("DeparturePlaceFilter: End")
