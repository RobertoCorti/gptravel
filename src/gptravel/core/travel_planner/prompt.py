from abc import ABC, abstractmethod
from inspect import cleandoc
from typing import Dict


class Prompt(ABC):
    def __init__(self, prompt: str) -> None:
        self._prompt = prompt

    @property
    def prompt(self) -> str:
        return cleandoc(self._prompt)

    @abstractmethod
    @property
    def json_keys(self) -> Dict[str, int]:
        pass


class PlainTravelPrompt(Prompt):
    def __init__(
        self, starting_travel_place: str, travel_destination: str, n_travel_days: int
    ) -> None:
        prompt = f"""Please generate a JSON with inside a travel plan of {n_travel_days} days for a person who wants to visit {travel_destination}.
                    The traveler leaves {starting_travel_place}. The structure of the JSON must be the following:
                    {{"Day x": {{"City": ["activity 1", "activity2",...]}}, "Day x+1": {{"City": []}}}}"""
        super().__init__(prompt)

    @property
    def json_keys(self) -> Dict[str, int]:
        return {"day": 0, "city": 1}
