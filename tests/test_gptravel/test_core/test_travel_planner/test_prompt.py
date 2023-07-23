from typing import Any, Dict

from gptravel.core.travel_planner.prompt import (
    CompletionTravelPrompt,
    PlainTravelPrompt,
    PromptFactory,
    ThematicTravelPrompt,
)
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class TestPrompt:
    def test_plain_prompt_from_factory(
        self, travel_properties: Dict[str, Any], prompt_factory: PromptFactory
    ):
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert isinstance(prompt_class, PlainTravelPrompt)
        travel_properties["travel_theme"] = None
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert isinstance(prompt_class, PlainTravelPrompt)

    def test_thematic_prompt_from_factory(
        self, travel_properties: Dict[str, Any], prompt_factory: PromptFactory
    ):
        travel_properties["travel_theme"] = "romantic"
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert isinstance(prompt_class, ThematicTravelPrompt)
        assert prompt_class.json_keys == {"day": 0, "city": 1}

    def test_completion_travel_prompt_from_factory(
        self,
        travel_properties: Dict[str, Any],
        prompt_factory: PromptFactory,
        travel_plan_single_city_per_day: TravelPlanJSON,
    ):
        travel_properties["complention_travel_plan"] = True
        travel_properties["n_days_to_add"] = 1
        travel_properties["travel_plan"] = travel_plan_single_city_per_day.travel_plan
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert prompt_class.json_keys == {"day": 0, "city": 1}
        assert isinstance(prompt_class, CompletionTravelPrompt)
        travel_properties["complention_travel_plan"] = False
        prompt_class = prompt_factory.build_prompt(**travel_properties)
        assert not isinstance(prompt_class, CompletionTravelPrompt)

    def test_properties(
        self, travel_properties: Dict[str, Any], prompt_factory: PromptFactory
    ):
        prompt = prompt_factory.build_prompt(**travel_properties)
        assert prompt.departure_place == travel_properties["departure_place"]
        assert prompt.destination_place == travel_properties["destination_place"]
        assert prompt.n_travel_days == travel_properties["n_travel_days"]
