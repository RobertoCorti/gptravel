from typing import Dict, Optional

import pytest

from gptravel.core.services.engine.entity_recognizer import EntityRecognizer


@pytest.fixture()
def recognizer() -> EntityRecognizer:
    return EntityRecognizer()


class TestEntityRecognizer:
    def test_property(self, recognizer: EntityRecognizer):
        assert recognizer.nlp

    @pytest.mark.parametrize(
        "input_text, expected_result",
        [
            ("I went to visit the Duomo", None),  # {"Duomo": "ORG"}),
            ("I went to visit the Duomo of Milan", {"the Duomo of Milan": "ORG"}),
            ("I ate a good pizza", None),
            (
                "Visit the Ein Gedi Nature Reserve for playing video games",
                {"the Ein Gedi Nature Reserve": "ORG"},
            ),
            ("Experience the refreshing waterfalls", None),
            ("Visit Jaffa Old City", None),  # {"Old City": "GPE"}),
            (
                "Visit the Stella Maris Monastery",
                None,
            ),  # {"the Stella Maris Monastery": "ORG"}),
            ("Enjoy a sunset at Jaffa Port", {"Jaffa Port": "FAC"}),
        ],
    )
    def test_recognize(
        self,
        recognizer: EntityRecognizer,
        input_text: str,
        expected_result: Optional[Dict[str, str]],
    ):
        assert recognizer.recognize(input_text) == expected_result

    @pytest.mark.parametrize(
        "input_code, expected_result",
        [
            ("GPE", "Countries, cities, states"),
            ("NNP", "noun, proper singular"),
            ("LOC", "Non-GPE locations, mountain ranges, bodies of water"),
            ("FAC", "Buildings, airports, highways, bridges, etc."),
            ("ORG", "Companies, agencies, institutions, etc."),
            ("BOTTLE", None),
        ],
    )
    def test_explain_code(
        self,
        recognizer: EntityRecognizer,
        input_code: str,
        expected_result: Optional[str],
    ):
        assert recognizer.explain(input_code) == expected_result
