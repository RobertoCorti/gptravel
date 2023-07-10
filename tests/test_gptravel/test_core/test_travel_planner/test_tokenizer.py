import pytest

from gptravel.core.travel_planner.token_manager import ChatGptTokenManager


@pytest.fixture
def chatgpt_token_manager() -> ChatGptTokenManager:
    return ChatGptTokenManager()


@pytest.mark.parametrize(
    "n_days, distance, expected",
    [(10, 100, 757), (0, 0, 383), (10, 5000, 756), (-100000000, 5, 383)],
)
def test_chatgpt_token_manager(
    chatgpt_token_manager: ChatGptTokenManager,
    n_days: int,
    distance: float,
    expected: int,
):
    result = chatgpt_token_manager.get_number_tokens(n_days=n_days, distance=distance)
    assert result == pytest.approx(expected, 1)
