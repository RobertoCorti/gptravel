from abc import ABC, abstractmethod
from typing import Any, Dict, List

from gptravel.core.travel_planner.prompt import Prompt
from gptravel.core.utils.general import (
    extract_inner_list_for_given_key,
    extract_inner_lists_from_json,
    extract_keys_by_depth_from_json,
)
from gptravel.core.utils.regex_tool import JsonExtractor


class TravelPlanJSON:
    def __init__(
        self,
        departure_place: str,
        destination_place: str,
        n_days: int,
        travel_plan_json: Dict[Any, Any],
        json_keys_depth_map: Dict[str, int],
    ) -> None:
        self._n_days = n_days
        self._departure_place = departure_place
        self._destination_place = destination_place
        self._travel_plan = travel_plan_json
        self._keys_map = json_keys_depth_map

    @property
    def departure_place(self) -> str:
        return self._departure_place

    @property
    def destination_place(self) -> str:
        return self._destination_place

    @property
    def n_days(self) -> int:
        return self._n_days

    @property
    def travel_plan(self) -> Dict[Any, Any]:
        return self._travel_plan

    @property
    def keys_map(self) -> Dict[str, int]:
        return self._keys_map

    @property
    def travel_activities(self) -> List[str]:
        return extract_inner_lists_from_json(self._travel_plan)

    def get_key_values_by_depth(self, depth: int) -> List[Any]:
        return extract_keys_by_depth_from_json(json_obj=self._travel_plan, ndepth=depth)

    def get_key_values_by_name(self, key_name: str) -> List[Any]:
        try:
            return self.get_key_values_by_depth(self._keys_map[key_name])
        except KeyError:
            return []

    def get_travel_activities_from_city(self, city_name: str) -> List[Any]:
        return extract_inner_list_for_given_key(self._travel_plan, key=city_name)

    @property
    def travel_cities(self) -> List[str]:
        return self.get_key_values_by_name("city")


class TravelEngine(ABC):
    def __init__(self) -> None:
        self._regex = JsonExtractor()

    @abstractmethod
    def get_travel_plan_json(self, prompt: Prompt) -> TravelPlanJSON:
        pass
