from typing import Any, Dict

import pytest

from gptravel.core.travel_planner.prompt import (
    PlainTravelPrompt,
    PromptFactory,
    ThematicTravelPrompt,
)


class TestPrompt:
    def test_plain_prompt_from_factory(
        self, travel_properties: Dict[str, Any], prompt_factory: PromptFactory
    ):
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert type(prompt_class) == PlainTravelPrompt
        travel_properties["travel_theme"] = None
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert type(prompt_class) == PlainTravelPrompt

    def test_thematic_prompt_from_factory(
        self, travel_properties: Dict[str, Any], prompt_factory: PromptFactory
    ):
        travel_properties["travel_theme"] = "romantic"
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert type(prompt_class) == ThematicTravelPrompt

    def test_properties(
        self, travel_properties: Dict[str, Any], prompt_factory: PromptFactory
    ):
        prompt = prompt_factory.build_prompt(**travel_properties)
        assert prompt.departure_place == travel_properties["departure_place"]
        assert prompt.destination_place == travel_properties["destination_place"]
        assert prompt.n_travel_days == travel_properties["n_travel_days"]
