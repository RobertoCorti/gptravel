import pytest

from gptravel.core.travel_planner.tokenizer import ChatGptTokenizer


@pytest.fixture
def chatgpt_tokenizer() -> ChatGptTokenizer:
    return ChatGptTokenizer()


@pytest.mark.parametrize(
    "n_days, distance, expected",
    [(10, 100, 757), (0, 0, 383), (10, 5000, 756), (-100000000, 5, 383)],
)
def test_chatgpt_tokenizer(
    chatgpt_tokenizer: ChatGptTokenizer, n_days: int, distance: float, expected: int
):
    result = chatgpt_tokenizer.get_number_tokens(n_days=n_days, distance=distance)
    assert result == pytest.approx(expected, 1)
