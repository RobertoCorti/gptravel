import pytest

from gptravel.core.utils.regex import JsonExtractor


@pytest.fixture
def extractor() -> JsonExtractor:
    return JsonExtractor()
