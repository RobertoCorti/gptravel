import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

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
    ) -> Optional[Dict[str, Dict[str, float]]]:
        pass


class ZeroShotTextClassifier(TextClassifier):
    def __init__(self, multi_label: bool = True) -> None:
        super().__init__(multi_label)
        self._api_token = os.getenv("HUGGING_FACE_KEY")

    def _query(self, payload: Dict[str, Any], api_url: str) -> List[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {self._api_token}"}
        logger.debug("HuggingFace API fetching response: start")
        response = requests.post(
            api_url, headers=headers, json=payload, timeout=50
        ).json()
        logger.debug("HuggingFace API fetching response: complete")
        if not isinstance(response, list):
            logger.error(
                "Hugging Face classifier: error in retrieving API response from %s",
                api_url,
            )
            logger.error("API respone: %s", response)
            raise HuggingFaceError
        return response

    def _predict(
        self,
        input_text_list: List[str],
        label_classes: List[str],
        api_url: str,
    ) -> Dict[str, Dict[str, float]]:
        payload = {
            "inputs": input_text_list,
            "parameters": {
                "candidate_labels": label_classes,
                "multi_label": self._multi_label,
            },
        }
        response = self._query(payload=payload, api_url=api_url)
        return {
            item["sequence"]: {
                label: float(value)
                for label, value in zip(item["labels"], item["scores"])
            }
            for item in response
        }

    def predict(
        self, input_text_list: List[str], label_classes: List[str]
    ) -> Optional[Dict[str, Dict[str, float]]]:
        api_url_list = [
            "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
            "https://api-inference.huggingface.co/models/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
            "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli",
        ]
        for api_url in api_url_list:
            try:
                output = self._predict(
                    input_text_list=input_text_list,
                    label_classes=label_classes,
                    api_url=api_url,
                )
                logger.debug("Using response from API url: %s", api_url)
                return output
            except HuggingFaceError:
                pass
            except requests.exceptions.ReadTimeout:
                pass
        return None
