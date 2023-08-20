import os

import pytest

from gptravel.core.services.engine.classifier import ZeroShotTextClassifier


@pytest.fixture()
def classifier() -> ZeroShotTextClassifier:
    return ZeroShotTextClassifier(multi_label=True)


@pytest.mark.skipif(
    os.getenv("HUGGING_FACE_KEY", "") == "", reason="no api key available"
)
class TestZeroShotClassifier:
    def test_property(self, classifier: ZeroShotTextClassifier):
        assert classifier.multi_label
        classifier.multi_label = False
        assert not classifier.multi_label

    def test_prediction(self, classifier: ZeroShotTextClassifier):
        labels = ["sea", "land", "city"]
        input_text = ["fish"]
        out = classifier.predict(input_text_list=input_text, label_classes=labels)[
            input_text[0]
        ]
        for label in labels:
            assert (out[label] < 1) & (out[label] >= 0)
        assert max(out, key=out.get) == "sea"
