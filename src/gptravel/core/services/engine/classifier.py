import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from gptravel.core.io.loggerconfig import logger
from gptravel.core.services.engine.exception import HuggingFaceError

load_dotenv()


class TextClassifier(ABC):
    def __init__(self, multi_label: bool) -> None:
        self.multi_label = multi_label

    @property
    def multi_label(self) -> bool:
        return self._multi_label

    @multi_label.setter
    def multi_label(self, multi_label: bool) -> None:
        self._multi_label = multi_label

    @abstractmethod
    def predict(
        self, input_text_list: List[str], label_classes: List[str]
    ) -> Dict[str, Dict[str, float]]:
        pass


class ZeroShotTextClassifier(TextClassifier):
    def __init__(self, multi_label: bool = True) -> None:
        super().__init__(multi_label)
        self._api_token = os.getenv("HUGGING_FACE_KEY")

    def _query(self, payload: Dict[str, Any], api_url: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self._api_token}"}
        logger.debug("HuggingFace API fetching response: start")
        response = requests.post(
            api_url, headers=headers, json=payload, timeout=20
        ).json()
        logger.debug("HuggingFace API fetching response: complete")
        return response

    def _query_on_different_apis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        api_urls = [
            "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
            "https://api-inference.huggingface.co/models/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
            "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli",
        ]
        for api_url in api_urls:
            response = self._query(payload=payload, api_url=api_url)
            if isinstance(response, list):
                logger.debug("Using response from API url: %s", api_url)
                return response
        return response

    def predict(
        self,
        input_text_list: List[str],
        label_classes: List[str],
    ) -> Dict[str, Dict[str, float]]:
        payload = {
            "inputs": input_text_list,
            "parameters": {
                "candidate_labels": label_classes,
                "multi_label": self._multi_label,
            },
        }
        try:
            response = self._query_on_different_apis(payload=payload)
            return {
                item["sequence"]: {
                    label: float(value)
                    for label, value in zip(item["labels"], item["scores"])
                }
                for item in response
            }
        except Exception as exc:
            logger.error("Hugging Face classifier: error in retrieving API response")
            raise HuggingFaceError from exc
