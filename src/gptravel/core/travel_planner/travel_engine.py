from abc import ABC, abstractmethod
from typing import Any, Dict

from gptravel.core.travel_planner.prompt import Prompt
from gptravel.core.utils.regex import JsonExtractor


class TravelPlanJSON:
    def __init__(
        self, travel_plan_json: Dict[Any, Any], json_keys: Dict[str, int]
    ) -> None:
        self._travel_plan = travel_plan_json
        self._keys = json_keys

    @property
    def travel_plan(self) -> Dict[Any, Any]:
        return self._travel_plan

    @property
    def keys(self) -> Dict[str, int]:
        return self._keys


class TravelEngine(ABC):
    def __init__(self) -> None:
        self._regex = JsonExtractor()

    @abstractmethod
    def get_travel_plan_json(self, prompt: Prompt) -> TravelPlanJSON:
        pass
