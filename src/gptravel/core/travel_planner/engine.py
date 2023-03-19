from abc import ABC, abstractmethod
from typing import Any, Dict, List

import openai

from gptravel.core.travel_planner.prompt import Prompt


class TravelEngine(ABC):
    @abstractmethod
    def get_travel_plan_json(self, prompt: Prompt) -> Dict[str, Dict[str, List[str]]]:
        pass


class OpenAIModel:
    def __init__(
        self,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
    ) -> None:
        assert presence_penalty >= 0.0 & presence_penalty <= 2.0
        assert frequency_penalty >= 0.0 & frequency_penalty <= 2.0
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._top_p = top_p
        self._frequency_penalty = frequency_penalty
        self._presence_penalty = presence_penalty

    def _openai_call(self, prompt: Prompt) -> Dict[Any, Any]:
        return openai.Completion.create(
            model=self._model,
            prompt=prompt.prompt,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p,
            frequency_penalty=self._frequency_penalty,
            presence_penalty=self._presence_penalty,
        )


class ChatGPTEngine(TravelEngine, OpenAIModel):
    def __init__(
        self,
        temperature: float,
        max_tokens: int,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
    ) -> None:
        model = "gpt-3.5-turbo"
        super().__init__(
            model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty
        )
