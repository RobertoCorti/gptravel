from typing import Dict, Optional

import spacy
from spacy.language import Language

from gptravel.core.io.loggerconfig import logger


class EntityRecognizer:
    def __init__(self, trained_pipeline: str = "en_core_web_sm") -> None:
        self._nlp = None
        try:
            self._nlp = spacy.load(trained_pipeline)
        except OSError:
            logger.warning(
                "%s trained pipeline is not available -- installing it",
                trained_pipeline,
            )
            import subprocess
            import sys

            subprocess.check_call(
                [sys.executable, "-m", "spacy", "download", trained_pipeline]
            )
            self._nlp = spacy.load(trained_pipeline)

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
