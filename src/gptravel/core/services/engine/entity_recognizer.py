from typing import Dict, Optional

import spacy
from spacy.language import Language

from gptravel.core.io.loggerconfig import logger


class EntityRecognizer:
    def __init__(self) -> None:
        self._nlp = None
        try:
            self._nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("en_core_web_sm trained pipeline is not available")

    @property
    def nlp(self) -> Optional[Language]:
        return self._nlp

    def explain(self, code_class: str) -> Optional[str]:
        return spacy.explain(code_class)

    def recognize(self, input_string: str) -> Optional[Dict[str, str]]:
        if self._nlp is not None:
            doc = self._nlp(input_string)
            if doc.ents:
                return {ent.text: ent.label_ for ent in doc.ents}
        return None
