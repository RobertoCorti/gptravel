from typing import Dict, Optional

import spacy
from spacy.language import Language

from gptravel.core.io.loggerconfig import logger

RECOGNIZED_ENTITIES_CACHE = {}


class EntityRecognizer:
    def __init__(self, trained_pipeline: str = "en_core_web_md") -> None:
        self._nlp = None
        try:
            self._nlp = spacy.load(
                trained_pipeline,
                disable=[
                    "tok2vec",
                    "tagger",
                    "parser",
                    "attribute_ruler",
                    "lemmatizer",
                ],
            )
        except OSError:
            logger.warning("%s trained pipeline is not available", trained_pipeline)

    @property
    def nlp(self) -> Optional[Language]:
        return self._nlp

    def explain(self, code_class: str) -> Optional[str]:
        return spacy.explain(code_class)

    def recognize(self, input_string: str) -> Optional[Dict[str, str]]:
        if self._nlp is not None:
            if input_string not in RECOGNIZED_ENTITIES_CACHE:
                RECOGNIZED_ENTITIES_CACHE[input_string] = self._nlp(input_string).ents
            if RECOGNIZED_ENTITIES_CACHE[input_string]:
                return {
                    ent.text: ent.label_
                    for ent in RECOGNIZED_ENTITIES_CACHE[input_string]
                }
        return None
