from abc import ABC, abstractmethod
from typing import Any, Dict, List

from gptravel.core.travel_planner.prompt import Prompt
from gptravel.core.utils.general import (
    extract_inner_lists_from_json,
    extract_keys_by_depth_from_json,
)
from gptravel.core.utils.regex import JsonExtractor


class TravelPlanJSON:
    def __init__(
        self, travel_plan_json: Dict[Any, Any], json_keys_depth_map: Dict[str, int]
    ) -> None:
        self._travel_plan = travel_plan_json
        self._keys_map = json_keys_depth_map

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


class TravelEngine(ABC):
    def __init__(self) -> None:
        self._regex = JsonExtractor()

    @abstractmethod
    def get_travel_plan_json(self, prompt: Prompt) -> TravelPlanJSON:
        pass
