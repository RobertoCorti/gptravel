from typing import Any, Dict

import pytest

from gptravel.core.travel_planner.prompt import (
    PlainTravelPrompt,
    PromptFactory,
    ThematicTravelPrompt,
)


def test_plain_prompt_from_factory(
    travel_properties: Dict[str, Any], prompt_factory: PromptFactory
):
    prompt_class = prompt_factory.build_prompt(**travel_properties)
    assert type(prompt_class) == PlainTravelPrompt
    travel_properties["travel_theme"] = None
    prompt_class = prompt_factory.build_prompt(**travel_properties)
    assert type(prompt_class) == PlainTravelPrompt


def test_thematic_prompt_from_factory(
    travel_properties: Dict[str, Any], prompt_factory: PromptFactory
):
    travel_properties["travel_theme"] = "romantic"
    prompt_class = prompt_factory.build_prompt(**travel_properties)
    assert type(prompt_class) == ThematicTravelPrompt
