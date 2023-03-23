import pytest

from gptravel.core.services.score_service import TravelPlanScore


@pytest.fixture
def score():
    score = TravelPlanScore()
    score.add_score("type score", {"score_value": 100, "score_weight": 0.11})
    score.add_score("score livel", {"score_value": 80, "score_weight": 0.23})
    score.add_score("score basso", {"score_value": 60, "score_weight": 0.15})
    return score


def test_add_score(score):
    score.add_score("score extra", {"score_value": 90, "score_weight": 0.10})
    assert score.score_map["score extra"] == {"score_value": 90, "score_weight": 0.10}


def test_weighted_score(score):
    assert score.weighted_score == pytest.approx(78.367, 0.001)


def test_weighted_score_empty():
    score = TravelPlanScore()
    assert score.weighted_score == None


def test_add_score_missing_key():
    score = TravelPlanScore()
    with pytest.raises(AssertionError):
        score.add_score("score extra", {"score_value": 90})
