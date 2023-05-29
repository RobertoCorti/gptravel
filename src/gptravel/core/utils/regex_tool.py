from typing import List

import regex


class JsonExtractor:
    def __init__(self) -> None:
        self._pattern = regex.compile(r"\{(?:[^{}]|(?R))*\}")

    def __call__(self, text: str) -> List[str]:
        return self._pattern.findall(text)
