from abc import ABC, abstractmethod
from typing import Dict, List

from gptravel.core.travel_planner.prompt import Prompt
from gptravel.core.utils.regex import JsonExtractor


class TravelEngine(ABC):
    def __init__(self) -> None:
        self._regex = JsonExtractor()

    @abstractmethod
    def get_travel_plan_json(self, prompt: Prompt) -> Dict[str, Dict[str, List[str]]]:
        pass
