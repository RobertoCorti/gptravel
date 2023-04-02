from abc import ABC, abstractmethod
from collections import defaultdict
from inspect import cleandoc
from typing import Dict


class Prompt(ABC):
    def __init__(self, prompt: str) -> None:
        self._prompt = prompt

    @property
    def prompt(self) -> str:
        return cleandoc(self._prompt)

    @property
    @abstractmethod
    def json_keys(self) -> Dict[str, int]:
        pass


class PlainTravelPrompt(Prompt):
    def __init__(
        self,
        travel_departure: str,
        travel_destination: str,
        n_travel_days: int,
        **kwargs,
    ) -> None:
        prompt = f"""Generate a JSON with inside a travel plan of {n_travel_days} days for a person who wants to visit {travel_destination} from
          {travel_departure}. The structure of the JSON must be the following:
          {{"Day x": {{"City": ["activity 1", "activity2",...], "City": ["activity 1", ...]}} , "Day x+1": {{"City": [...], "City": [...]}} }} 
          where City field is the city visited in the corresponding Day. A possible activity could be the transport from one City to another."""
        super().__init__(prompt)

    @property
    def json_keys(self) -> Dict[str, int]:
        return {"day": 0, "city": 1}


class ThematicTravelPrompt(Prompt):
    def __init__(
        self,
        travel_departure: str,
        travel_destination: str,
        n_travel_days: int,
        travel_theme: str,
        **kwargs,
    ) -> None:
        prompt = f"""Generate a JSON with inside a travel plan of {n_travel_days} days for a person who wants to visit {travel_destination} from
          {travel_departure}. The theme of the travel is {travel_theme}.
          The structure of the JSON must be the following:
          {{"Day x": {{"City": ["activity 1", "activity2",...], "City": ["activity 1", ...]}} , "Day x+1": {{"City": [...], "City": [...]}} }} 
          where City field is the city visited in the corresponding Day. A possible activity could be the transport from one City to another."""
        super().__init__(prompt)

    @property
    def json_keys(self) -> Dict[str, int]:
        return {"day": 0, "city": 1}


class PromptFactory:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build_prompt(**kwargs) -> Prompt:
        kwargs = defaultdict(str, kwargs)
        if kwargs["travel_theme"]:
            return ThematicTravelPrompt(**kwargs)
        else:
            return PlainTravelPrompt(**kwargs)
